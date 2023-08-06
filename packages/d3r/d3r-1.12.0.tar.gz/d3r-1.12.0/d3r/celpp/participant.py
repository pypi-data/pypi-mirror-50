# -*- coding: utf-8 -*-

__author__ = 'churas'

import logging
import re

logger = logging.getLogger(__name__)


class Participant(object):
    """Represents a an external participant in the challenge
    """

    def __init__(self, name, d3rusername, guid, email,
                 priority=0):
        """Constructor
        :param name: Full name of participant
        :param d3rusername: D3R username
        :param guid: unique id given to participant
        :param email: participant email address
        :param priority: int defining priority participants docked
                         results should be evaluated. default is 0
                         and higher values have higher priority
        :raises ValueError: if priority is set to a non int value
        """
        self._name = name
        self._d3rusername = d3rusername
        self._guid = guid
        self._email = email
        self._priority = int(priority)

    def get_name(self):
        """Gets name
        """
        return self._name

    def get_d3rusername(self):
        """Gets d3rusername
        """
        return self._d3rusername

    def get_guid(self):
        """Gets guid
        """
        return self._guid

    def get_email(self):
        """Gets email
        """
        return self._email

    def get_priority(self):
        """Gets priority for Participant used
           in determining order evaluations are run
        :returns: int denoting priority with higher
                  numbers meaning higher priority
        """
        return self._priority


class ParticipantDatabase(object):
    """Database object that contains a set of `Participants`
    """

    def __init__(self, participants):
        """Constructor
        :param participants: List of participants
        """
        self._participants = participants

    def get_participant_by_guid(self, guid,
                                exact_match=False):
        """Searches database for `Participant` with matching `guid`
        :param guid: guid or unique id for `Participant`
        :param exact_match: if set to True only guid matching
                            exactly with a `Participant` will be returned.
                            If False then the method will try for an exact
                            match, but if that fails the first `Participant`
                            that matches guid if _# is tripped of is used.
        :returns `Participant` with matching `guid` or None if not found
        """
        if guid is None:
            logger.warning('guid passed in was None')
            return None

        if self._participants is None:
            logger.warning('participants is None')
            return None

        for p in self._participants:
            if p.get_guid() == guid:
                return p

        if exact_match is True:
            logger.debug('No match found and exact_match is set '
                         'to True. returning None for guid: ' + guid)
            return None

        # TODO This wont work if the participant guids become a
        # TODO length other then 5 digits ie #####_XXXXX
        possible_guids = re.findall('([0-9]{5})_[0-9A-Za-z-]+$', guid)
        if len(possible_guids) is not 1:
            logger.debug('Stripped guid ' + guid +
                         ' did not yield single answer but this ' +
                         str(possible_guids))
            return None
        stripped_guid = possible_guids[0]
        if stripped_guid != guid:
            logger.debug('Stripped guid is different: ' + stripped_guid +
                         'performing search again')
            for p in self._participants:
                if p.get_guid() == stripped_guid:
                    return p

        return None

    def get_participants(self):
        """Gets participants as list
        :returns: List of `Participants`
        """
        return self._participants


class ParticipantDatabaseFromCSVFactory(object):
    """Factory class that generates `ParticipantDatabase` object from CSV file
    """

    def __init__(self, csvfile):
        """Constructor that takes CSV file `csvfile` to generate
        `ParticipantDatabase` object.  The format of the CSV file
        is as follows:

        name,d3rusername,guid,email
        bob smith,bsmith,8675309,bob@bob.com

        :param csvfile: Path to `Participant` CSV file
        """
        self._csvfile = csvfile

    def get_participant_database(self):
        """Parses CSV file set in constructor to create `ParticipantDatabase`
        :returns `ParticipantDatabase` from CSV file or None if there was an
        error
        """
        if self._csvfile is None:
            logger.warning('No csv file set')
            return None
        try:
            f = open(self._csvfile, 'rU')
            counter = 0
            plist = []
            for line in f:
                if counter is 0:
                    if line.startswith('name'):
                        logger.debug('Skipping header line')
                        counter = + 1
                        continue

                splitline = line.rstrip().split(',')
                split_len = len(splitline)
                if split_len is not 4 and split_len is not 5:
                    logger.warning('Problems splitting line ' + line +
                                   ' got ' + str(len(splitline)) +
                                   ' elements expecting 4 or 5 fields'
                                   ' name,username,guid,email or '
                                   ' name,username,guid,email,priority')
                    counter = + 1
                    continue
                priority = 0

                if split_len is 5:
                    try:
                        priority = int(splitline[4].rstrip())
                    except ValueError:
                        logger.error('Expected int for priority got: ' +
                                     splitline[4].rstrip())
                        pass

                plist.append(Participant(splitline[0].strip(),
                                         splitline[1].strip(),
                                         splitline[2].strip(),
                                         splitline[3].strip(),
                                         priority=priority))
                counter = + 1
            f.close()
            return ParticipantDatabase(plist)
        except Exception:
            logger.exception('Caught exception')
        return None
