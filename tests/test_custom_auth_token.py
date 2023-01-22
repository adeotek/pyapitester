import unittest
from datetime import datetime, timedelta
from src.apitester import custom_auth_token


class TestCustomAuthToken(unittest.TestCase):
    
    def test_generate_token_and_validate_token_valid_true(self):
        clientId = 'UnitTest-' + datetime.utcnow().strftime('%y%m%d%H%M%S') + '-'
        secretKey = 'some-long-secret-key-shared-between-client-and-server'
        serverId = 'unit-test-service-api'
        validity = 15
        token, expiresAt = custom_auth_token.generate_token(secretKey, clientId, serverId, validity)
        result, tokenClientId, message = custom_auth_token.validate_token(token, secretKey, serverId)
        self.assertTrue(result)
        self.assertTrue(datetime.utcnow() <= expiresAt)
        self.assertEqual(clientId, tokenClientId)
        self.assertEqual('', message)

    def test_generate_token_with_valid_input_expect_valid_token(self):
        clientId = 'UnitTest-' + datetime.utcnow().strftime('%y%m%d%H%M%S') + '-'
        secretKey = 'some-long-secret-key-shared-between-client-and-server'
        serverId = 'unit-test-service-api'
        validity = 15
        expectedResult = '84eb5aa661e8a3e313b525ab69c38cc8d54c47830ea18f40e795af8d5263575c'
        token, expiresAt = custom_auth_token.generate_token(secretKey, clientId, serverId, validity)
        expiresAtToken = expiresAt.strftime('%Y-%m-%dT%H:%M:%S').encode('ascii').hex().lower()
        self.assertEqual(clientId + expectedResult + expiresAtToken, token)

    def test_generate_token_with_invalid_secret_key_expect_ValueError(self):
        clientId = 'UnitTest-' + datetime.utcnow().strftime('%y%m%d%H%M%S') + '-'
        secretKey = ''
        serverId = 'unit-test-service-api'
        validity = 15
        with self.assertRaises(ValueError):
            custom_auth_token.generate_token(secretKey, clientId, serverId, validity)

    def test_validate_token_with_empty_token_expect_ValueError(self):
        secretKey = 'some-long-secret-key-shared-between-client-and-server'
        serverId = 'unit-test-service-api'
        token = ''
        result, clientId, message = custom_auth_token.validate_token(token, secretKey, serverId)
        self.assertFalse(result)
        self.assertEqual(None, clientId)
        self.assertEqual('Invalid token value/size!', message)
    
    def test_validate_token_with_non_string_token_expect_ValueError(self):
        secretKey = 'some-long-secret-key-shared-between-client-and-server'
        serverId = 'unit-test-service-api'
        token = ['not valid']
        result, clientId, message = custom_auth_token.validate_token(token, secretKey, serverId)
        self.assertFalse(result)
        self.assertEqual(None, clientId)
        self.assertEqual('Invalid token value/size!', message)

    def test_validate_token_with_invalid_secret_key_expect_ValueError(self):
        secretKey = ''
        serverId = 'unit-test-service-api'
        token = '000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
        result, clientId, message = custom_auth_token.validate_token(token, secretKey, serverId)
        self.assertFalse(result)
        self.assertEqual(None, clientId)
        self.assertEqual('Invalid `secretKey` value!', message)

    def test_validate_token_with_valid_token_expect_true(self):
        clientId = 'UnitTest-' + datetime.utcnow().strftime('%y%m%d%H%M%S') + '-'
        secretKey = 'some-long-secret-key-shared-between-client-and-server'
        serverId = 'unit-test-service-api'
        validity = 15
        expiresAt = datetime.now() + timedelta(minutes=validity)
        expiresAtToken = expiresAt.strftime('%Y-%m-%dT%H:%M:%S').encode('ascii').hex().lower()
        token = clientId + '84eb5aa661e8a3e313b525ab69c38cc8d54c47830ea18f40e795af8d5263575c' + expiresAtToken
        result, tokenClientId, message = custom_auth_token.validate_token(token, secretKey, serverId)
        self.assertTrue(result)
        self.assertEqual(clientId, tokenClientId)
        self.assertEqual('', message)


if __name__ == '__main__':
    unittest.main()
