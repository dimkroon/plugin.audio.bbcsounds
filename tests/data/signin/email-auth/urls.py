# ------------------------------------------------------------------------------
#  Copyright (c) 2026 Dimitri Kroon.
#  This file is part of plugin.audio.bbcsounds.
#  SPDX-License-Identifier: GPL-3.0-or-later
#  See LICENSE.txt or https://www.gnu.org/licenses/gpl-3.0.txt
# ------------------------------------------------------------------------------

requests = {
    '1': {
        'comment': 'first request to the login page',
        'method': 'get',
        'resp': 302,
        'url': 'https://account.bbc.com/auth?context=sounds&journeyGroupType=sign-in&redirectUri=https%3A%2F%2Fsession.bbc.co.uk%2Fsession%2Fcallback%3Frealm%3D%2F&sequenceId=a633f6ab-543f-406a-9f50-e261099de462',
        'params': {
            'context': 'sounds',
            'journeyGroupType': 'sign-in',
            'redirectUri': 'https://session.bbc.co.uk/session/callback?realm=/',
            'sequenceId': 'a633f6ab-543f-406a-9f50-e261099de462'
        }

    },
    '1a': {
        'comment': 'redirect to session page to pick up some cookies and a nonce as querystring parameter',
        'method': 'get',
        'resp': 302,
        'url': 'https://session.bbc.co.uk/session?visitor_id=87e01687-cc01-44f8-9fe1-91ce6ab3cbd2&context=sounds&journeyGroupType=sign-in&redirectUri=https%3A%2F%2Fsession.bbc.co.uk%2Fsession%2Fcallback%3Frealm%3D%2F&sequenceId=a633f6ab-543f-406a-9f50-e261099de462',
        'params': {
            'visitor_id': '87e01687-cc01-44f8-9fe1-91ce6ab3cbd2',
            'context': 'sounds',
            'journeyGroupType': 'sign-in',
            'redirectUri': 'https://session.bbc.co.uk/session/callback?realm=/',
            'sequenceId': 'a633f6ab-543f-406a-9f50-e261099de462'
        }
    },
    '1b': {
        'comment': "redirect to the entry page to enter one's email address",
        'method': 'get',
        'resp': 200,
        'url': 'https://account.bbc.com/auth?realm=%2F&clientId=Account&context=sounds&journeyGroupType=sign-in&sequenceId=a633f6ab-543f-406a-9f50-e261099de462&isCasso=false&action=sign-in&redirectUri=https%3A%2F%2Fsession.bbc.co.uk%2Fsession%2Fcallback%3Frealm%3D%2F&service=IdSignInService&nonce=8tqbOVlp-TYVVGo4ZrHIpPEORWA7A-ycsDeo',
        'params': {
            "action": "sign-in",
            "clientId": "Account",
            "context": "sounds",
            "isCasso": "false",
            "journeyGroupType": "sign-in",
            "nonce": "8tqbOVlp-TYVVGo4ZrHIpPEORWA7A-ycsDeo",
            "realm": "/",
            "redirectUri": "https://session.bbc.co.uk/session/callback?realm=/",
            "sequenceId": "a633f6ab-543f-406a-9f50-e261099de462",
            "service": "IdSignInService",

        }
    },
    '2': {
        'comment': 'submit the email address',
        'method': 'post',
        'resp': 200,
        'url': 'https://account.bbc.com/auth?action=sign-in&clientId=Account&context=sounds&isCasso=false&journeyGroupType=sign-in&nonce=8tqbOVlp-TYVVGo4ZrHIpPEORWA7A-ycsDeo&realm=%2F&redirectUri=https%3A%2F%2Fsession.bbc.co.uk%2Fsession%2Fcallback%3Frealm%3D%2F&sequenceId=a633f6ab-543f-406a-9f50-e261099de462&service=IdSignInService',
        'params': {
            "action": "sign-in",
            "clientId": "Account",
            "context": "sounds",
            "isCasso": "false",
            "journeyGroupType": "sign-in",
            "nonce": "8tqbOVlp-TYVVGo4ZrHIpPEORWA7A-ycsDeo",
            "realm": "/",
            "redirectUri": "https://session.bbc.co.uk/session/callback?realm=/",
            "sequenceId": "a633f6ab-543f-406a-9f50-e261099de462",
            "service": "IdSignInService"
        }
    },
    '3': {
        'comment': 'hit button to send email with link',
        'method': 'post',
        'resp': 200,
        'url': 'https://account.bbc.com/auth?userJourney=magicLink&action=sign-in&clientId=Account&context=sounds&isCasso=false&journeyGroupType=sign-in&nonce=8tqbOVlp-TYVVGo4ZrHIpPEORWA7A-ycsDeo&realm=%2F&redirectUri=https%3A%2F%2Fsession.bbc.co.uk%2Fsession%2Fcallback%3Frealm%3D%2F&sequenceId=a633f6ab-543f-406a-9f50-e261099de462&service=IdSignInService',
        'params': {
            "userJourney": "magicLink",
            "action": "sign-in",
            "clientId": "Account",
            "context": "sounds",
            "isCasso": "false",
            "journeyGroupType": "sign-in",
            "nonce": "8tqbOVlp-TYVVGo4ZrHIpPEORWA7A-ycsDeo",
            "realm": "/",
            "redirectUri": "https://session.bbc.co.uk/session/callback?realm=/",
            "sequenceId": "a633f6ab-543f-406a-9f50-e261099de462",
            "service": "IdSignInService"
        }
    },
    '4': {
        'comment': 'poll for link to be clicked',
        'method': 'post',
        'resp': 401,
        'url': 'https://account.bbc.com/api/magic-link/authenticate?authorise=true&action=sign-in&clientId=Account&context=sounds&isCasso=false&journeyGroupType=sign-in&nonce=8tqbOVlp-TYVVGo4ZrHIpPEORWA7A-ycsDeo&realm=%2F&redirectUri=https%3A%2F%2Fsession.bbc.co.uk%2Fsession%2Fcallback%3Frealm%3D%2F&sequenceId=a633f6ab-543f-406a-9f50-e261099de462&service=IdSignInService&showExperimentError=false&userJourney=magicLink',
        'params': {
            "showExperimentError": "false",
            "authorise": "true",
            "userJourney": "magicLink",
            "action": "sign-in",
            "clientId": "Account",
            "context": "sounds",
            "isCasso": "false",
            "journeyGroupType": "sign-in",
            "nonce": "8tqbOVlp-TYVVGo4ZrHIpPEORWA7A-ycsDeo",
            "realm": "/",
            "redirectUri": "https://session.bbc.co.uk/session/callback?realm=/",
            "sequenceId": "a633f6ab-543f-406a-9f50-e261099de462",
            "service": "IdSignInService",
        }
    },
    'failed_test': {
        'status': 403,
        'url': 'https://account.bbc.com/api/magic-link/auhtenticate?authorise=true&userJourney=magicLink&showExperimentError=false&jsEnabled=false&action=sign-in&clientId=Account&isCasso=false&journeyGroupType=sign-in&nonce=Zd3N8tQH-kc_wjrtitQ3ZKwgWFTfK2hQ-Afg&ptrt=https%3A%2F%2Fwww.bbc.co.uk%2F&realm=%2F&redirectUri=https%3A%2F%2Fsession.bbc.co.uk%2Fsession%2Fcallback%3Frealm%3D%2F&sequenceId=c85949f0-1966-4140-a8af-adcf6f828d4c&service=IdSignInService',
        'params': {
            "showExperimentError": "false",
            "authorise": "true",
            "userJourney": "magicLink",
            "jsEnabled": "false",
            "action": "sign-in",
            "clientId": "Account",
            "isCasso": "false",
            "journeyGroupType": "sign-in",
            "nonce": "Zd3N8tQH-kc_wjrtitQ3ZKwgWFTfK2hQ-Afg",
            "ptrt": "https://www.bbc.co.uk/",
            "realm": "/",
            "redirectUri": "https://session.bbc.co.uk/session/callback?realm=/",
            "sequenceId": "c85949f0-1966-4140-a8af-adcf6f828d4c",
            "service": "IdSignInService"
        }
    },
    'new_email_send': {
        'url': 'https://account.bbc.com/auth?userJourney=magicLink&action=sign-in&clientId=Account&isCasso=false&journeyGroupType=sign-in&nonce=Z9CqZulX-YGb5pRVdaCnaNAMY7P1Yke0cP1A&realm=%2F&redirectUri=https%3A%2F%2Fsession.bbc.co.uk%2Fsession%2Fcallback%3Frealm%3D%2F&sequenceId=523a7153-8458-4ae4-a519-8376df4338a6&service=IdSignInService'
    }

}
