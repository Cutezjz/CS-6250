import logging
import os
import re

from fixture import TESTING_FIXTURE

test_names = sorted(TESTING_FIXTURE.keys())
FORMAT = '%(asctime)-15s | %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('multi_topology_test')
logger.setLevel(logging.INFO)


def get_green(string):
    '''Return string with green font'''
    return '\033[92m{}\033[00m'.format(string)


def get_red(string):
    '''Return string with red font'''
    return '\033[91m{}\033[00m'.format(string)


def get_dist_vector_dict(lines):
    '''Get a distance vector dictionary from a list of lines
    :param lines: All the lines from a log file
    :returns: dist_vectors -- the distance vectors represented by the lines
    '''
    dist_vectors = dict()
    for line in lines:
        parts = line.split(':')
        key = parts[0]
        distances = parts[1].split(',')
        dist_tuples = []
        for vector in distances:
            cost = re.search('(?=\d)\d*$', vector).group(0)
            cost_num = int(cost)
            destination = vector[:vector.find(cost)]
            dist_tuples.append((destination, cost_num))
        dist_vectors[key] = dict((dst, cost) for dst, cost in dist_tuples)
    return dist_vectors


def get_last_pass(lines):
    '''Get the last pass from the log file produced by running a topology
    :param lines: All the lines from the log file
    :returns: list -- the list of lines just before the final "-----" line.
    '''
    indices = [i for i, line in enumerate(lines) if line == '-----']
    if len(indices) == 1:
        return lines[:indices[0]]
    else:
        return lines[indices[-2] + 1: indices[-1]]


# Alright, now go through each topology and ensure the final pass in the log
# matches the expected values.
for topology in test_names:
    # Step 1: Read this topology's correct distance vectors into a dict.
    expected_dist_vectors = get_dist_vector_dict(TESTING_FIXTURE[topology])

    # Step 2: Run the topology using our run.sh script.
    assert os.path.isfile('./{}.py'.format(topology)),\
        'File [{}.py] must be in the same directory as run.sh'.format(topology)
    os.system('./run.sh {} > /dev/null 2>&1'.format(topology))

    # Step 3: Now read the created log file into a different dict.
    with open('{}.log'.format(topology), 'rb') as curr_log:
        log_lines = [line.strip() for line in curr_log.readlines()]
        trimmed_lines = get_last_pass(log_lines)
        actual_dist_vectors = get_dist_vector_dict(trimmed_lines)

    # Step 4: Log whether or not the two dictionaries are equivalent.
    status = None
    if (actual_dist_vectors == expected_dist_vectors):
        status = get_green('PASSED')
        logger.info('Running file {:35}| {}'.format(topology + '.py', status))
    else:
        status = get_red('FAILED')
        logger.warning(
            'Running file {:35}| {}'.format(topology + '.py', status))
