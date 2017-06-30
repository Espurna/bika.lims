from Products.CMFCore.utils import getToolByName
from DateTime import DateTime

from bika.lims import logger
from bika.lims.workflow import doActionFor
from bika.lims.workflow import getCurrentState
from bika.lims.workflow import isBasicTransitionAllowed


def _cascade_transition(obj, transition_id):
    """ Performs the transition for the transition_id passed in to children
    :param obj: Sample for which the transition has to be cascaded
    :param transition_id: Unique id of the transition
    """
    # Sample all obj partitions
    # Note the transition for SamplePartition already transitions all the
    # analyses associated to that Sample partition, so there is no need to
    # transition all the analyses from Sample here.
    for part in obj.objectValues('SamplePartition'):
        doActionFor(part, transition_id)

    # when a obj is sampled, all associated
    # AnalysisRequests are also transitioned
    for ar in obj.getAnalysisRequests():
        doActionFor(ar, transition_id)


def after_no_sampling_workflow(obj):
    """Method triggered after a 'no_sampling_workflow' transition for the
    Sample passed in is performed. Triggers the 'no_sampling_workflow'
    transition for dependent objects, such as Sample Partitions and
    Analysis Requests.
    This function is called automatically by
    bika.lims.workflow.AfterTransitionEventHandler
    :param obj: Sample affected by the transition
    :type obj: Sample
    """
    _cascade_transition(obj, 'no_sampling_workflow')


def after_sampling_workflow(obj):
    """Method triggered after a 'sampling_workflow' transition for the Sample
    passed in is performed. Triggers the 'sampling_workflow' transition for
    dependent objects, such as Sample Partitions and Analysis Requests.
    This function is called automatically by
    bika.lims.workflow.AfterTransitionEventHandler
    :param obj: Sample affected by the transition
    :type obj: Sample
    """
    _cascade_transition(obj, 'sampling_workflow')


def after_to_be_preserved(obj):
    """Method triggered after a 'to_be_preserved' transition for the Sample
    passed in is performed. Triggers the 'to_be_preserved' transition for
    dependent objects, such as Sample Partitions and Analysis Requests.
    This function is called automatically by
    bika.lims.workflow.AfterTransitionEventHandler
    :param obj: Sample affected by the transition
    :type obj: Sample
    """
    _cascade_transition(obj, 'to_be_preserved')


def after_preserve(obj):
    """Method triggered after a 'preserve' transition for the Sample passed
    in is performed. Triggers the 'preserve' transition for dependent objects,
    such as Sample Partitions and Analysis Requests.
    This function is called automatically by
    bika.lims.workflow.AfterTransitionEventHandler
    :param obj: Sample affected by the transition
    :type obj: Sample
    """
    _cascade_transition(obj, 'preserve')


def after_schedule_sampling(obj):
    """Method triggered after a 'schedule_sampling' transition for the Sample
    passed in is performed. Triggers the 'cancel' transition for dependent
    objects, such as Sample Partitions and Analysis Requests.
    This function is called automatically by
    bika.lims.workflow.AfterTransitionEventHandler
    :param obj: Sample affected by the transition
    :type obj: Sample
    """
    _cascade_transition(obj, 'schedule_sampling')


def after_sample(obj):
    """Method triggered after a 'sample' transition for the Sample passed in.
    Triggers the 'sample' transition for dependent objects, such as Sample
    Partitions and Analysis Requests.
    This function is called automatically by
    bika.lims.workflow.AfterTransitionEventHandler
    :param obj: Sample affected by the transition
    :type obj: Sample
    """
    _cascade_transition(obj, 'sample')


def after_sample_due(obj):
    """Method triggered after a 'sample_due' transition for the Sample passed
    in is performed. Triggers the 'sample_due' transition for dependent
    objects, such as Sample Partitions and Analysis Requests.
    This function is called automatically by
    bika.lims.workflow.AfterTransitionEventHandler
    :param obj: Sample affected by the transition
    :type obj: Sample
    """
    _cascade_transition(obj, 'sample_due')


def after_receive(obj):
    """Method triggered after a 'receive' transition for the Sample passed in
    is performed. Stores value for "Date Received" field and also triggers the
    'receive' transition for dependent objects, such as Sample Partitions and
    Analysis Requests.
    This function is called automatically by
    bika.lims.workflow.AfterTransitionEventHandler
    :param obj: Sample affected by the transition
    :type obj: Sample
    """
    # In most cases, the date of a given transition can be retrieved from an
    # object by using a getter that delegates the action to getTransitionDate,
    # without the need of storing the value manually.
    # This is a diifferent case: a DateTimeField/Widget field is explicitly
    # declared in Sample's schema becaise in some cases, the user may want to
    # change the Received Date by him/herself. For this reason, we set the
    # value manually here.
    obj.setDateReceived(DateTime())
    obj.reindexObject(idxs=["getDateReceived", ])
    _cascade_transition(obj, 'receive')


def after_reject(obj):
    """Method triggered after a 'reject' transition for the Sample passed in is
    performed. Transitions children (Analysis Requests and Sample Partitions)
    bika.lims.workflow.AfterTransitionEventHandler
    :param obj: Sample affected by the transition
    :type obj: Sample
    """
    ars = obj.getAnalysisRequests()
    for ar in ars:
        if getCurrentState(ar) != 'rejected':
            doActionFor(ar, 'reject')
            reasons = obj.getRejectionReasons()
            ar.setRejectionReasons(reasons)

    parts = obj.objectValues('SamplePartition')
    for part in parts:
        if getCurrentState(part) != 'rejected':
            doActionFor(part, "reject")


def after_dispose(obj):
    """Method triggered after a 'dispose' transition for the Sample passed in
    is performed. Stores value for "Date Disposed" field
    This function is called automatically by
    bika.lims.workflow.AfterTransitionEventHandler
    :param obj: Sample affected by the transition
    :type obj: Sample
    """
    obj.setDateDisposed(DateTime())
    obj.reindexObject(idxs=["getDateDisposed", ])


def after_reinstate(obj):
    """Method triggered after a 'reinstate' transition for the Sample passed in
    is performed. Triggers the 'reinstate' transition for dependent objects,
    such as Sample Partitions and Analysis Requests.
    This function is called automatically by
    bika.lims.workflow.AfterTransitionEventHandler
    :param obj: Sample affected by the transition
    :type obj: Sample
    """
    _cascade_transition(obj, 'reinstate')


def after_expire(obj):
    """Method triggered after a 'exipre' transition for the Sample passed in
    is performed. Stores value for "Date Expired" field
    This function is called automatically by
    bika.lims.workflow.AfterTransitionEventHandler
    :param obj: Sample affected by the transition
    :type obj: Sample
    """
    obj.setDateExpired(DateTime())
    obj.reindexObject(idxs=["getDateExpired", ])


def after_cancel(obj):
    """Method triggered after a 'cancel' transition for the Sample passed in is
    performed. Triggers the 'cancel' transition for dependent objects, such
    as Sample Partitions and Analysis Requests.
    This function is called automatically by
    bika.lims.workflow.AfterTransitionEventHandler
    :param obj: Sample affected by the transition
    :type obj: Sample
    """
    _cascade_transition(obj, 'cancel')
