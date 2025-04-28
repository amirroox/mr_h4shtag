from m_plotMsg.core.safe import Arbn

def test_arbn_initialization():
    arbn = Arbn()
    assert arbn.example_method() == "Hello from Arbn!"