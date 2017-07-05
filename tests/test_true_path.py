import true_path


def test_true_path():
    # Correct one, non-verbose
    assert true_path.safe_url("https://www.example.com/@2")
    # Non-safe protocol
    assert not true_path.safe_url("http://www.example.com/@2")
    # No protocol declared
    assert not true_path.safe_url("www.example.com/@2")
    # Wrong structure
    assert not true_path.safe_url("Lorem ipsum dolor sit amet")
    # Unwanted prefix
    assert not true_path.safe_url("alamakotahttps://www.example.com")


def test_true_path_verbose():
    # Correct one, verbose
    assert true_path.safe_url("https://www.example.com/@2", True)
    # Non-safe protocol, verbose
    assert not true_path.safe_url("http://www.example.com/@2", verbose=True)
    # No protocol declared, verbose
    assert not true_path.safe_url("www.example.com/@2", True)
    # Wrong structure, verbose
    assert not true_path.safe_url("Lorem ipsum dolor sit amet", True)


def test_safe_certificate():
    assert true_path.safe_certificate("https://www.example.com/", True)
    assert not true_path.safe_certificate("https://expired.badssl.com/")
    assert not true_path.safe_certificate("http://www.onet.pl")  # no https
    assert not true_path.safe_certificate("ala ma kota")  # invalid argument


def test_popular_site():
    assert true_path.popular_site("https://aliorbank.pl/hades/do/Login",
                                  verbose=True)  # primary use – OK
    assert not true_path.popular_site(
        "http://parafia.czeladz.pl/administrator/artykul.html", verbose=True)
    # It simply can't be popular ;)
    assert true_path.popular_site("https://konto.onet.pl/auth.html?app_id="
                                  "poczta.onet.pl.front.onetapi.pl")


def test_google_safe_browsing():
    assert not true_path.google_safe_browsing("http://www.ianfette.org/")
    # The Internet says, it's fake "dangerous" website run by Google.
    # Maybe better do not check...?
    assert true_path.google_safe_browsing(
        "https://aliorbank.pl/hades/do/Login", verbose=True)
    # primary use – OK


def test_suite():
    assert true_path.suite("https://www.google.com", True)
    assert not true_path.suite("http://www.google.com")  # No HTTPS


def test_cli():
    from click.testing import CliRunner
    from true_path import cli
    runner = CliRunner()

    # assert execution without verbosity
    result = runner.invoke(cli.main, ["https://www.google.com"])
    assert result.exit_code == 0

    # assert execution without verbosity
    result = runner.invoke(cli.main, ["https://www.google.com", "-v"])
    assert result.exit_code == 0

    # assert '--help  Show this message and exit.' in help_result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
