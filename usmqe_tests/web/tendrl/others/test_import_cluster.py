"""
Description: Simple log in test

Author: ltrilety
"""


import pytest

from usmqe.web.tendrl.mainpage.navpage.pages import NavMenuBars
from usmqe.web.tendrl.mainpage.clusters.cluster_list.pages import ClustersList
from usmqe.web.tendrl.mainpage.landing_page.pages import get_landing_page
from usmqe.web.tendrl.auxiliary.pages import UpperMenu


def test_initial_import_cluster(log_in, log_out):
    """ positive import cluster test
    """
    home_page = log_in.init_object
    pytest.check(home_page._label == 'home page',
                 'Tendrl should route to home page'
                 ' if there is no cluster present',
                 hard=True)

    home_page.import_gluster_cluster()
# TODO: Wait till the cluster is imported, check task
#       When finished, remove following line(s)
#       https://github.com/Tendrl/usmqe-tests/issues/33
    import time
    time.sleep(180)
    # log out and log in again
    upper_menu = UpperMenu(log_in.driver)
    upper_menu.open_user_menu().logout()
    log_in.loginpage.login_user(
        pytest.config.getini("usm_username"),
        pytest.config.getini("usm_password"))
    # or just go to the default URL
    # log_in.driver.get(pytest.config.getini("usm_web_url"))
    home_page = get_landing_page(log_in.driver)

    pytest.check(home_page._label == 'main page - menu bar',
                 'Tendrl should not route to home page any more',
                 hard=True)
    NavMenuBars(log_in.driver).open_clusters(click_only=True)
    cluster_list = ClustersList(log_in.driver)
# TODO: Check that correct cluster is present in the list
    pytest.check(len(cluster_list) == 1,
                 'There should be exactly one cluster in tendrl')
