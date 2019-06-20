import math
import sys


class VectorCompare:
    def magnitude(self, concordance):
        total = 0
        for word, count in concordance.items():
            total += count ** 2
        return math.sqrt(total)

    def relation(self, concordance1, concordance2):
        topvalue = 0
        for word, count in concordance1.items():
            if word in concordance2:
                topvalue += count * concordance2[word]
        if (self.magnitude(concordance1) * self.magnitude(concordance2)) != 0:
            return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))
        else:
            return 0

    def concordance(self, document):
        con = {}
        for word in document.split(' '):
            if word in con:
                con[word] = con[word] + 1
            else:
                con[word] = 1
        return con


def find_best_match(keywords, conversation, responses):
    v = VectorCompare()

    matches = []

    for x in responses:
        relation = v.relation(v.concordance(conversation[x]['keywords']), v.concordance(keywords))

        if relation != 0:
            matches.append((relation, x))

    matches.sort(reverse=True)

    if len(matches) != 0:
        return matches[0][1]

    return None


def find_loose_match(keywords, conversation):
    v = VectorCompare()

    matches = []

    for key, value in conversation.items():
        relation = v.relation(v.concordance(' '.join([value['keywords'], value['opening'], value['title']])), v.concordance(keywords))
        if relation != 0:
            matches.append((relation, value))

    matches.sort(reverse=True)

    if len(matches) != 0:
        return matches

    return None


if __name__ == '__main__':
    conversation = {
        'start': {
            'opening': 'Hello! RCC (really cheap chatbot) here what are you trying to do today? At any time type quit to quit.',
            'responses': ['pay-bill-online', 'change-address', 'what-we-do', 'history', 'pay-bill-credit-card', 'pay-bill-paypal'],
            'keywords': '',
            'title': ''
        },
        'pay-bill-online': {
            'opening': 'Do you want to pay your bill using a credit card or using paypal?',
            'keywords': 'i am looking pay a bill online Do you want to pay your bill using a credit card or using paypal? pay pal',
            'responses': ['pay-bill-credit-card', 'pay-bill-paypal'],
            'title': 'Pay a bill online'
        },
        'history': {
            'keywords': 'Would you like to know about the history of Us',
            'opening': '''We're the leading Australian company supplying things to 4.2 million customers and developing and producing natural widgets. We also aspire to be the number one plumbus company in Australia.''',
            'responses': [],
            'title': 'Learn about the history of us'
        },
        'what-we-do': {
            'keywords': 'Would you like to know what we do?',
            'opening': '''Being integrated, we hav diverse operations spanning across the plumbus supply chain, from plumbus production, to widget retailing.''',
            'responses': [],
            'title': 'Learn about what we do'
        },
        'pay-bill-credit-card': {
            'keywords': 'i want to pay using visa mastercard american express amex credit card',
            'opening': 'You can pay online using your credit card at https://plumbus.com.au/pay',
            'responses': [],
            'title': 'Pay a bill by credit card'
        },
        'pay-bill-paypal': {
            'keywords': 'i would like to pay a bill online using paypal pay pal',
            'opening': 'You can pay online using paypal at https://plumbus.com.au/paypal',
            'responses': [],
            'title': 'Pay a bill using Paypal'
        },
        'change-address': {
            'keywords': 'i want to change move my home address',
            'opening': 'Great! You can change your home address by calling one of our friendly consultants on 13-13-13 anytime 24/7',
            'responses': [],
            'title': 'Change my home address'
        },
    }

    run = True
    current_state = 'start'
    response = ''

    while run:
        if response and response.lower() == 'quit':
            run = False
            sys.exit()

        if conversation[current_state]['responses']:
            response = input(conversation[current_state]['opening'] + ': ')
            desired_state = find_best_match(response, conversation, conversation[current_state]['responses'])

            if desired_state:
                current_state = desired_state
            else:
                loose = find_loose_match(response, conversation)

                if loose:
                    print('''Sorry I did't quite catch what you were saying. We you trying to do one of the following?''')
                    for x in loose:
                        print(x[1]['title'])
                else:
                    print('''Sorry I did't quite catch what you were saying. Could you try typing it using different words please.''')
        else:
            print(conversation[current_state]['opening'])
            response = 'quit'
        print('')
        if desired_state:
            current_state = desired_state
