ADA = "text-ada-001"
BABBAGE = "text-babbage-001"
CURIE = "text-curie-001"
DAVINCI = "text-davinci-003"

ADA_UNIT_COST = 0.0004
BABBAGE_UNIT_COST = 0.0005
CURIE_UNIT_COST = 0.0020
DAVINCI_UNIT_COST = 0.0200


def log_cost(completion, total):

    print('> ↑' + str(completion.usage.prompt_tokens) + ' ↓' +
          str(completion.usage.completion_tokens) + ' (=' + str(completion.usage.total_tokens) + ')')

    unit_cost = 0

    if completion.model == ADA:
        unit_cost = ADA_UNIT_COST
    elif completion.model == BABBAGE:
        unit_cost = BABBAGE_UNIT_COST
    elif completion.model == CURIE:
        unit_cost = CURIE_UNIT_COST
    elif completion.model == DAVINCI:
        unit_cost = DAVINCI_UNIT_COST

    total.append((completion.usage.total_tokens,
                 unit_cost * completion.usage.total_tokens / 1000.0))
