import json
import pytest

from cranc import cranc

@pytest.mark.parametrize('status', ('Open', 'Closed', 'Merged'))
def test_filter_pull_requests(status):
    data = cranc.filter_pull_requests(status, None, None)
    for pr in data:
        assert pr['status'] == status 
        

