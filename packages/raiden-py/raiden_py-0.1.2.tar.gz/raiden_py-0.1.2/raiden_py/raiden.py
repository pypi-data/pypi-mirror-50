import requests


class RaidenException(Exception):
    def __init__(self, status_code, body=''):
        self.status_code = status_code
        self.body = body

    def __str__(self):
        return repr("API failure: status_code: {}, body: {}".format(self.status_code, self.body))


class Raiden:
    def __init__(self, base_url, version):
        """
        API DOC (https://raiden-network.readthedocs.io/en/stable/rest_api.html)

        Args:
            base_url (str): base url e.g. http://localhost:5001
            version (str): version of the raiden api e.g. v1
        """
        self.version = version
        self.base_url = base_url
        self.api_url = '{base_url}/api/{version}'.format(**{
            'base_url': base_url,
            'version': version
        })

    def send_request(self, request_method, api_type, data=None):
        """
        Send request

        Args:
            request_method (str): GET, POST, PUT, PATCH or DELETE
            api_type (str): raiden api type e.g. address
            data (dict): data dict for the request

        Returns:
            response (requests.models.Response): Response object

        Raises:
            RaidenException (raiden_py.raiden.RaidenException): raised if response status code is not 2XX
        """
        data = data or {}
        url = '{api_url}/{api_type}'.format(**{
            'api_url': self.api_url,
            'api_type': api_type
        })
        headers = {"Content-Type": "application/json"}
        if request_method == 'GET':
            response = requests.get(url, params=data)
        elif request_method == 'POST':
            response = requests.post(url=url, headers=headers, json=data)
        elif request_method == 'PUT':
            response = requests.put(url=url, headers=headers, json=data)
        elif request_method == 'DELETE':
            response = requests.delete(url=url, headers=headers, json=data)
        elif request_method == 'PATCH':
            response = requests.patch(url=url, headers=headers, json=data)
        else:
            raise ValueError("request method not supported")
        if response.status_code not in [200, 201]:
            raise RaidenException(status_code=response.status_code, body=response.text)
        return response

    def get_address(self):
        """
        Query your address. When raiden starts, you choose an ethereum address which will also be your raiden address.

        Returns:
            response (dict): Raiden Node info dict

                             {
                                "our_address": "0x2a65Aca4D5fC5B5C859090a6c34d164135398226"
                             }

        Raises:
            RaidenException (raiden_py.raiden.RaidenException): raised if response status code is not 2XX

        """
        response = self.send_request(request_method='GET', api_type='address')
        return response.json()

    def register_token(self, token_address):
        """
        Register a token

        Args:
            token_address (str): token address

        Returns:
            response (dict): response dict

                             {
                                "token_network_address": "0xC4F8393fb7971E8B299bC1b302F85BfFB3a1275a"
                             }

        Raises:
            RaidenException (raiden_py.raiden.RaidenException): raised if response status code is not 2XX

        """
        api_type = 'tokens/{token_address}'.format(**{
            "token_address": token_address
        })
        response = self.send_request(request_method='PUT', api_type=api_type)
        return response.json()

    def get_channels(self):
        """
        Get a list of all unsettled channels.

        Returns:
            response (list): list of all unsettled channels

                             [
                                {
                                    "token_network_identifier": "0xE5637F0103794C7e05469A9964E4563089a5E6f2",
                                    "channel_identifier": 20,
                                    "partner_address": "0x61C808D82A3Ac53231750daDc13c777b59310bD9",
                                    "token_address": "0xEA674fdDe714fd979de3EdF0F56AA9716B898ec8",
                                    "balance": 25000000,
                                    "total_deposit": 35000000,
                                    "state": "opened",
                                    "settle_timeout": 100,
                                    "reveal_timeout": 30
                                }
                            ]

        Raises:
            RaidenException (raiden_py.raiden.RaidenException): raised if response status code is not 2XX

        """
        response = self.send_request(request_method='GET', api_type='channels')
        return response.json()

    def get_channels_token(self, token_address):
        """
        Get a list of all unsettled channels for the given token address.

        Args:
            token_address (str): token address

        Returns:
            response (list): list of all unsettled channels for the given token address

                             [
                                {
                                    "token_network_identifier": "0xE5637F0103794C7e05469A9964E4563089a5E6f2",
                                    "channel_identifier": 20,
                                    "partner_address": "0x61C808D82A3Ac53231750daDc13c777b59310bD9",
                                    "token_address": "0xEA674fdDe714fd979de3EdF0F56AA9716B898ec8",
                                    "balance": 25000000,
                                    "total_deposit": 35000000,
                                    "state": "opened",
                                    "settle_timeout": 100,
                                    "reveal_timeout": 30
                                }
                             ]

        Raises:
            RaidenException (raiden_py.raiden.RaidenException): raised if response status code is not 2XX
        """
        api_type = 'channels/{token_address}'.format(**{
            "token_address": token_address
        })
        response = self.send_request(request_method='GET', api_type=api_type)
        return response.json()

    def get_channel_info(self, token_address, partner_address):
        """
        Query information about one of your channels.
        The channel is specified by the address of the token and the partner’s address.

        Args:
            token_address (str): token address
            partner_address (str): partner address

        Returns:
            response (dict): channel_info dict

                             {
                                "token_network_identifier": "0xE5637F0103794C7e05469A9964E4563089a5E6f2",
                                "channel_identifier": 20,
                                "partner_address": "0x61C808D82A3Ac53231750daDc13c777b59310bD9",
                                "token_address": "0xEA674fdDe714fd979de3EdF0F56AA9716B898ec8",
                                "balance": 25000000,
                                "total_deposit": 35000000,
                                "state": "opened",
                                "settle_timeout": 100,
                                "reveal_timeout": 30
                            }

        Raises:
            RaidenException (raiden_py.raiden.RaidenException): raised if response status code is not 2XX
        """
        api_type = 'channels/{token_address}/{partner_address}'.format(**{
            "token_address": token_address,
            "partner_address": partner_address
        })
        response = self.send_request(request_method='GET', api_type=api_type)
        return response.json()

    def get_token_addresses(self):
        """
        Returns a list of addresses of all registered tokens.

        Returns:
            response (list): list of addresses of all registered tokens

                             [
                                "0xEA674fdDe714fd979de3EdF0F56AA9716B898ec8",
                                "0x61bB630D3B2e8eda0FC1d50F9f958eC02e3969F6"
                             ]

        Raises:
            RaidenException (raiden_py.raiden.RaidenException): raised if response status code is not 2XX

        """
        response = self.send_request(request_method='GET', api_type='tokens')
        return response.json()

    def get_token_network_address(self, token_address):
        """
        Returns the address of the corresponding token network for the given token, if the token is registered.

        Args:
            token_address (str): token address

        Returns:
            response (str): token network address

                            "0x61bB630D3B2e8eda0FC1d50F9f958eC02e3969F6"

        Raises:
            RaidenException (raiden_py.raiden.RaidenException): raised if response status code is not 2XX
        """
        api_type = 'tokens/{token_address}'.format(**{
            "token_address": token_address
        })
        response = self.send_request(request_method='GET', api_type=api_type)
        return response.text

    def get_partners(self, token_address):
        """
        Returns a list of all partners with whom you have non-settled channels for a certain token.

        Args:
            token_address (str): token address

        Returns:
            response (list): list of partners

                             [
                                {
                                   "partner_address": "0x2a65aca4d5fc5b5c859090a6c34d164135398226",
                                   "channel": "/api/<version>/channels/0x61C808D82A3Ac53231750daDc13c777b59310bD9/"
                                              "0x2a65aca4d5fc5b5c859090a6c34d164135398226"
                                }
                             ]

        Raises:
            RaidenException (raiden_py.raiden.RaidenException): raised if response status code is not 2XX
        """
        api_type = 'tokens/{token_address}/partners'.format(**{
            "token_address": token_address
        })
        response = self.send_request(request_method='GET', api_type=api_type)
        return response.json()

    def get_pending_transfers(self):
        """
        Returns a list of all transfers that have not been completed yet.

        Returns:
            response (list): list of all pending transfers

                             [
                               {
                                  "channel_identifier": "255",
                                  "initiator": "0x5E1a3601538f94c9e6D2B40F7589030ac5885FE7",
                                  "locked_amount": "119",
                                  "payment_identifier": "1",
                                  "role": "initiator",
                                  "target": "0x00AF5cBfc8dC76cd599aF623E60F763228906F3E",
                                  "token_address": "0xd0A1E359811322d97991E03f863a0C30C2cF029C",
                                  "token_network_identifier": "0x111157460c0F41EfD9107239B7864c062aA8B978",
                                  "transferred_amount": "331"
                               }

                             ]

        Raises:
            RaidenException (raiden_py.raiden.RaidenException): raised if response status code is not 2XX
        """
        api_type = 'pending_transfers'
        response = self.send_request(request_method='GET', api_type=api_type)
        return response.json()

    def get_pending_transfers_token(self, token_address):
        """
        Returns a list of all transfers that have not been completed yet for specified token

        Args:
            token_address (str): token address

        Returns:
            response (list): list of all pending transfers

                             [
                               {
                                  "channel_identifier": "255",
                                  "initiator": "0x5E1a3601538f94c9e6D2B40F7589030ac5885FE7",
                                  "locked_amount": "119",
                                  "payment_identifier": "1",
                                  "role": "initiator",
                                  "target": "0x00AF5cBfc8dC76cd599aF623E60F763228906F3E",
                                  "token_address": "0xd0A1E359811322d97991E03f863a0C30C2cF029C",
                                  "token_network_identifier": "0x111157460c0F41EfD9107239B7864c062aA8B978",
                                  "transferred_amount": "331"
                               }

                             ]

        Raises:
            RaidenException (raiden_py.raiden.RaidenException): raised if response status code is not 2XX
        """
        api_type = 'pending_transfers/{token_address}'.format(**{
            "token_address": token_address
        })
        response = self.send_request(request_method='GET', api_type=api_type)
        return response.json()

    def get_pending_transfers_channel(self, token_address, partner_address):
        """
        Returns a list of all transfers that have not been completed yet for specified channel

        Args:
            token_address (str): token address
            partner_address (str): partner address

        Returns:
            response (list): list of all pending transfers

                             [
                               {
                                  "channel_identifier": "255",
                                  "initiator": "0x5E1a3601538f94c9e6D2B40F7589030ac5885FE7",
                                  "locked_amount": "119",
                                  "payment_identifier": "1",
                                  "role": "initiator",
                                  "target": "0x00AF5cBfc8dC76cd599aF623E60F763228906F3E",
                                  "token_address": "0xd0A1E359811322d97991E03f863a0C30C2cF029C",
                                  "token_network_identifier": "0x111157460c0F41EfD9107239B7864c062aA8B978",
                                  "transferred_amount": "331"
                               }

                             ]

        Raises:
            RaidenException (raiden_py.raiden.RaidenException): raised if response status code is not 2XX
        """
        api_type = 'pending_transfers/{token_address}/{partner_address}'.format(**{
            "token_address": token_address,
            "partner_address": partner_address
        })
        response = self.send_request(request_method='GET', api_type=api_type)
        return response.json()

    def create_channel(self, token_address, partner_address, total_deposit, settle_timeout=500):
        """
        Create a channel

        Args:
            token_address (str): The token we want to be used in the channel.
            partner_address (str): The partner we want to open a channel with.
            total_deposit (int): Total amount of tokens to be deposited to the channel
            settle_timeout (int): The amount of blocks that the settle timeout should have

        Returns:
            response (dict): channel info dict

                                {
                                    "token_network_identifier": "0xE5637F0103794C7e05469A9964E4563089a5E6f2",
                                    "channel_identifier": 20,
                                    "partner_address": "0x61C808D82A3Ac53231750daDc13c777b59310bD9",
                                    "token_address": "0xEA674fdDe714fd979de3EdF0F56AA9716B898ec8",
                                    "balance": 25000000,
                                    "total_deposit": 35000000,
                                    "state": "opened",
                                    "settle_timeout": 500,
                                    "reveal_timeout": 30
                                }
        Raises:
            RaidenException (raiden_py.raiden.RaidenException): raised if response status code is not 2XX

        """
        api_type = 'channels'
        data = {
            "partner_address": partner_address,
            "token_address": token_address,
            "total_deposit": total_deposit,
            "settle_timeout": settle_timeout
        }
        response = self.send_request(request_method='PUT', api_type=api_type, data=data)
        return response.json()

    def close_channel(self, token_address, partner_address):
        """
        Close a channel

        Args:
            token_address (str): token address
            partner_address (str): partner address

        Returns:
            response (dict): channel info dict

                             {
                                "token_network_identifier": "0xE5637F0103794C7e05469A9964E4563089a5E6f2",
                                "channel_identifier": 20,
                                "partner_address": "0x61C808D82A3Ac53231750daDc13c777b59310bD9",
                                "token_address": "0xEA674fdDe714fd979de3EdF0F56AA9716B898ec8",
                                "balance": 25000000,
                                "total_deposit": 35000000,
                                "state": "closed",
                                "settle_timeout": 500,
                                "reveal_timeout": 30
                             }
        Raises:
            RaidenException (raiden_py.raiden.RaidenException): raised if response status code is not 2XX

        """
        api_type = 'channels/{token_address}/{partner_address}'.format(**{
            "token_address": token_address,
            "partner_address": partner_address
        })
        data = {
            "state": "closed"
        }
        response = self.send_request(request_method='PATCH', api_type=api_type, data=data)
        return response.json()

    def increase_deposit_channel(self, token_address, partner_address, total_deposit):
        """
        Increase the deposit in the channel

        Args:
            token_address (str): token address
            partner_address (str): partner address
            total_deposit (int): The increased total deposit

        Returns:
            response (dict): channel info dict

                             {
                                "token_network_identifier": "0xE5637F0103794C7e05469A9964E4563089a5E6f2",
                                "channel_identifier": 20,
                                "partner_address": "0x61C808D82A3Ac53231750daDc13c777b59310bD9",
                                "token_address": "0xEA674fdDe714fd979de3EdF0F56AA9716B898ec8",
                                "balance": 25000000,
                                "total_deposit": 35000000,
                                "state": "closed",
                                "settle_timeout": 500,
                                "reveal_timeout": 30
                             }
        Raises:
            RaidenException (raiden_py.raiden.RaidenException): raised if response status code is not 2XX

        """
        api_type = 'channels/{token_address}/{partner_address}'.format(**{
            "token_address": token_address,
            "partner_address": partner_address
        })
        data = {
            "total_deposit": total_deposit
        }
        response = self.send_request(request_method='PATCH', api_type=api_type, data=data)
        return response.json()

    def withdraw_token_channel(self, token_address, partner_address, total_withdraw):
        """
        Withdraw token

        Args:
            token_address (str): token address
            partner_address (str): partner address
            total_withdraw (int): The increased total withdraw

        Returns:
            response (dict): channel info dict

                             {
                                "token_network_address":"0xE5637F0103794C7e05469A9964E4563089a5E6f2",
                                "channel_identifier":20,
                                "partner_address":"0x61C808D82A3Ac53231750daDc13c777b59310bD9",
                                "token_address":"0xEA674fdDe714fd979de3EdF0F56AA9716B898ec8",
                                "balance":25000000,
                                "total_deposit":35000000,
                                "total_withdraw":5000000,
                                "state":"closed",
                                "settle_timeout":500,
                                "reveal_timeout":30
                             }

        Raises:
            RaidenException (raiden_py.raiden.RaidenException): raised if response status code is not 2XX

        """
        api_type = 'channels/{token_address}/{partner_address}'.format(**{
            "token_address": token_address,
            "partner_address": partner_address
        })
        data = {
            "total_withdraw": total_withdraw
        }
        response = self.send_request(request_method='PATCH', api_type=api_type, data=data)
        return response.json()

    def get_joined_token_networks(self):
        """
        Returns a dict containing all joined token networks.

        Returns:
            response (dict): dict containing all joined token networks
                             (each key is a token address for which you have open channels)

                             {
                                "0x2a65Aca4D5fC5B5C859090a6c34d164135398226": {
                                    "funds": 100,
                                    "sum_deposits": 67,
                                    "channels": 3
                                },
                                "0x0f114A1E9Db192502E7856309cc899952b3db1ED": {
                                    "funds": 49
                                    "sum_deposits": 31,
                                    "channels": 1
                                }
                             }

        Raises:
            RaidenException (raiden_py.raiden.RaidenException): raised if response status code is not 2XX
        """
        api_type = 'connections'
        response = self.send_request(request_method='GET', api_type=api_type)
        return response.json()

    def join_token_network(self, token_address, funds, initial_channel_target=3, joinable_funds_target=0.4):
        """
        Automatically join a token network. The request will only return once all blockchain calls
        for opening and/or depositing to a channel have completed.

        Args:
            token_address (str): token address
            funds (int): Amount of funding you want to put into the network
            initial_channel_target (int): Number of channels to open proactively
            joinable_funds_target (float): Fraction of funds that will be used to join channels opened by
                                           other participants.

        Returns:
            response (dict): response dict

        Raises:
            RaidenException (raiden_py.raiden.RaidenException): raised if response status code is not 2XX

        """
        api_type = 'connections/{token_address}'.format(**{
            "token_address": token_address
        })
        data = {
            "funds": funds,
            "initial_channel_target": initial_channel_target,
            "joinable_funds_target": joinable_funds_target
        }
        response = self.send_request(request_method='PUT', api_type=api_type, data=data)
        return response.json()

    def leave_token_network(self, token_address):
        """
        Leave a token network. The request will only return once all blockchain calls for closing/settling
        a channel have completed.

        Args:
            token_address (str): token address

        Returns:
            response (list): list with the addresses of all closed channels

                              [
                                "0x41BCBC2fD72a731bcc136Cf6F7442e9C19e9f313",
                                "0x5A5f458F6c1a034930E45dC9a64B99d7def06D7E",
                                "0x8942c06FaA74cEBFf7d55B79F9989AdfC85C6b85"
                              ]

        Raises:
            RaidenException (raiden_py.raiden.RaidenException): raised if response status code is not 2XX

        """
        api_type = 'connections/{token_address}'.format(**{
            "token_address": token_address
        })
        response = self.send_request(request_method='DELETE', api_type=api_type)
        return response.json()

    def initiate_payment(self, token_address, target_address, amount, identifier=0):
        """
        Initiate a payment. The request will only return once the payment either succeeded or failed.
        A payment can fail due to the expiration of a lock, the target being offline, channels on the path to the
        target not having enough settle_timeout and reveal_timeout in order to allow the payment to be propagated
        safely, not enough funds etc.

        Args:
            token_address (str): token address
            target_address (str): target address
            amount (int): Amount to be sent to the target
            identifier (int): Identifier of the payment (optional)

        Returns:
            response (dict): payment info dict

                              {
                                "initiator_address": "0xEA674fdDe714fd979de3EdF0F56AA9716B898ec8",
                                "target_address": "0x61C808D82A3Ac53231750daDc13c777b59310bD9",
                                "token_address": "0x2a65Aca4D5fC5B5C859090a6c34d164135398226",
                                "amount": 200,
                                "identifier": 42
                              }

        Raises:
            RaidenException (raiden_py.raiden.RaidenException): raised if response status code is not 2XX

        """
        api_type = 'payments/{token_address}/{target_address}'.format(**{
            "token_address": token_address,
            "target_address": target_address
        })
        data = {
            "amount": amount,
            "identifier": identifier
        }
        response = self.send_request(request_method='POST', api_type=api_type, data=data)
        return response.json()

    def get_payment_history(self, token_address, target_address):
        """
        Query the payment history. This includes successful (EventPaymentSentSuccess)
        and failed (EventPaymentSentFailed) sent payments as well as received payments (EventPaymentReceivedSuccess).

        Args:
            token_address (str): token address
            target_address (str): target address

        Returns:
            response (list): payment history list


                                [
                                    {
                                        "event": "EventPaymentReceivedSuccess",
                                        "amount": 5,
                                        "initiator": "0x82641569b2062B545431cF6D7F0A418582865ba7",
                                        "identifier": 1,
                                        "log_time": "2018-10-30T07:03:52.193"
                                    },
                                    {
                                        "event": "EventPaymentSentSuccess",
                                        "amount": 35,
                                        "target": "0x82641569b2062B545431cF6D7F0A418582865ba7",
                                        "identifier": 2,
                                        "log_time": "2018-10-30T07:04:22.293"
                                    },
                                    {
                                        "event": "EventPaymentSentSuccess",
                                        "amount": 20,
                                        "target": "0x82641569b2062B545431cF6D7F0A418582865ba7"
                                        "identifier": 3,
                                        "log_time": "2018-10-30T07:10:13.122"
                                    }
                                ]

        Raises:
            RaidenException (raiden_py.raiden.RaidenException): raised if response status code is not 2XX

        """
        api_type = 'payments/{token_address}/{target_address}'.format(**{
            "token_address": token_address,
            "target_address": target_address
        })
        response = self.send_request(request_method='GET', api_type=api_type)
        return response.json()
