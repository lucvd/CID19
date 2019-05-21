Feature: Navigate through Connect-ID site
    Scenario: can find search results
        When visit url "http://google.com"
        When field with name "q" is given "Connect-ID"
        Then title becomes "Connect-ID - Google Search"

