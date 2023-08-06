from drupal_hash_utility import DrupalHashUtility


def test_all():
    drash = DrupalHashUtility()
    password = 'P@ssw0rd'
    encode = drash.encode(password)
    hash_summary = drash.summary(encode)
    assert hash_summary['iterations'] and hash_summary['salt'] and hash_summary['hash']
    verify = drash.verify(password, encode)
    assert verify is True
