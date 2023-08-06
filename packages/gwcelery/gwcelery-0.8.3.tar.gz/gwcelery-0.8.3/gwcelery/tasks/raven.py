"""Search for GRB-GW coincidences with ligo-raven."""
import ligo.raven.search
from celery import chain
from ligo.gracedb.exceptions import HTTPError
from ligo.raven import gracedb_events

from ..import app
from . import gracedb
from . import ligo_fermi_skymaps


def calculate_coincidence_far(gracedb_id, group):
    """Compute temporal coincidence FAR for external trigger and superevent
    coincidence by calling ligo.raven.search.calc_signif_gracedb.

    Parameters
    ----------
    gracedb_id: str
        ID of the superevent trigger used by GraceDB
    group: str
        CBC or Burst; group of the preferred_event associated with the
        gracedb_id superevent
    """
    try:
        preferred_skymap = ligo_fermi_skymaps.get_preferred_skymap(gracedb_id)
    except ValueError:
        preferred_skymap = None

    em_events = gracedb.get_superevent(gracedb_id)['em_events']
    tl_cbc, th_cbc = app.conf['raven_coincidence_windows']['GRB_CBC']
    tl_burst, th_burst = app.conf['raven_coincidence_windows']['GRB_Burst']

    if group == 'CBC':
        tl, th = tl_cbc, th_cbc
    elif group == 'Burst':
        tl, th = tl_burst, th_burst

    canvas = chain()
    for exttrig_id in em_events:
        search = gracedb.get_event(exttrig_id)['search']
        try:
            ext_skymap = gracedb.download('glg_healpix_all_bn_v00.fit',
                                          exttrig_id)
        except HTTPError:
            ext_skymap = None
        if ext_skymap and preferred_skymap:
            canvas |= (
                calc_signif.si(gracedb_id, exttrig_id, tl, th,
                               search,
                               incl_sky=True,
                               se_fitsfile=preferred_skymap))
        else:
            canvas |= (
                calc_signif.si(gracedb_id, exttrig_id, tl, th, search,
                               incl_sky=False))
    return canvas


@app.task(shared=False)
def calc_signif(se_id, exttrig_id, tl, th, search, incl_sky, se_fitsfile=None):
    """Calculate FAR of GRB exttrig-GW coincidence"""
    return ligo.raven.search.calc_signif_gracedb(
        se_id, exttrig_id, tl, th, grb_search=search, se_fitsfile=se_fitsfile,
        incl_sky=incl_sky, gracedb=gracedb.client)


def coincidence_search(gracedb_id, alert_object, group=None, pipelines=[]):
    """Perform ligo-raven search for coincidences.
    The ligo.raven.search.search method applies EM_COINC label on its own.

    Parameters
    ----------
    gracedb_id: str
        ID of the trigger used by GraceDB
    alert_object: dict
        lvalert['object']
    group: str
        Burst or CBC
    pipelines: list
        list of external trigger pipeline names
    """

    tl_cbc, th_cbc = app.conf['raven_coincidence_windows']['GRB_CBC']
    tl_burst, th_burst = app.conf['raven_coincidence_windows']['GRB_Burst']
    tl_snews, th_snews = app.conf['raven_coincidence_windows']['SNEWS']

    if 'SNEWS' in pipelines:
        tl, th = tl_snews, th_snews
    elif group == 'CBC' and gracedb_id.startswith('E'):
        tl, th = tl_cbc, th_cbc
    elif group == 'CBC' and gracedb_id.startswith('S'):
        tl, th = -th_cbc, -tl_cbc
    elif group == 'Burst' and gracedb_id.startswith('E'):
        tl, th = tl_burst, th_burst
    elif group == 'Burst' and gracedb_id.startswith('S'):
        tl, th = -th_burst, -tl_burst
    else:
        raise ValueError('Invalid RAVEN search request for {0}'.format(
            gracedb_id))

    raven_search_results = search(gracedb_id, alert_object,
                                  tl, th, group, pipelines)
    add_exttrig_to_superevent(raven_search_results, gracedb_id)

    if gracedb_id.startswith('E') and raven_search_results:
        for search_result in raven_search_results:
            calculate_coincidence_far(
                search_result['superevent_id'], group).delay()
            gracedb.create_label.delay('EM_COINC',
                                       search_result['superevent_id'])
        gracedb.create_label.delay('EM_COINC', gracedb_id)

    elif raven_search_results:
        calculate_coincidence_far(gracedb_id, group).delay()
        for search_result in raven_search_results:
            gracedb.create_label.delay('EM_COINC', search_result['graceid'])
        gracedb.create_label.delay('EM_COINC', gracedb_id)


@app.task(shared=False)
def search(gracedb_id, alert_object, tl=-5, th=5, group=None,
           pipelines=[]):
    """Perform ligo-raven search for coincidences.
    The ligo.raven.search.search method applies EM_COINC label on its own.

    Parameters
    ----------
    gracedb_id: str
        ID of the trigger used by GraceDB
    alert_object: dict
        lvalert['object']
    tl: int
        number of seconds to search before
    th: int
        number of seconds to search after
    group: str
        Burst or CBC
    pipelines: list
        list of external trigger pipelines for performing coincidence search
        against
    Returns
    -------
        list with the dictionaries of related gracedb events
    """
    if alert_object.get('superevent_id'):
        event = gracedb_events.SE(gracedb_id, gracedb=gracedb.client)
        group = None
    else:
        event = gracedb_events.ExtTrig(gracedb_id, gracedb=gracedb.client)
        pipelines = []
    return ligo.raven.search.search(event, tl, th, gracedb=gracedb.client,
                                    group=group, pipelines=pipelines)


@app.task(shared=False)
def add_exttrig_to_superevent(raven_search_results, gracedb_id):
    """Add external trigger to the list of em_events after
    ligo.raven.search.search finds a coincidence

    Parameters
    ----------
    raven_search_results: list
        list of dictionaries of each related gracedb trigger
    gracedb_id: str
        ID of either a superevent or external trigger
    """
    # First determine whether the gracedb_id is for a superevent or exttrig
    if gracedb_id.startswith('E'):
        for superevent in raven_search_results:
            superevent_id = superevent['superevent_id']
            gracedb.add_event_to_superevent(superevent_id, gracedb_id)
    else:
        for exttrig in raven_search_results:
            exttrig_id = exttrig['graceid']
            gracedb.add_event_to_superevent(gracedb_id, exttrig_id)
