#!/usr/bin/python
#coding:utf-8
import argparse
import requests
import json
import os
import datetime
import pickle
import time
import csv
import copy

TODAY = datetime.datetime.now() - datetime.timedelta(days=1)

WeekInfo = {
    'W1': (20171017, 20171022),
    'W2': (20171023, 20171029),
    'W3': (20171030, 20171105),
    'W4': (20171106, 20171112),
    'W5': (20171113, 20171119),
    'W6': (20171120, 20171126),
    'W7': (20171127, 20171203),
    'W8': (20171204, 20171210),
    'W9': (20171211, 20171217),
    'W10': (20171218, 20171224),
    'W11': (20171225, 20171231),
    'W12': (20180101, 20180107),
    'W13': (20180108, 20180114),
    'W14': (20180115, 20180121),
    'W15': (20180122, 20180128),
    'W16': (20180129, 20180204),
    'W17': (20180205, 20180211),
    'W18': (20180212, 20180225),
    'W19': (20180226, 20180304),
    'W20': (20180305, 20180311),
    'W21': (20180312, 20180318),
    'W22': (20180319, 20180325),
    'W23': (20180326, 20180401),
    'W24': (20180402, 20180408),
    'W25': (20180409, 20180411)
}

NBATeamInfo = {
    
    'ATL': {'Name': 'HAWKS', 'TeamID': '1610612737'},
    'BOS': {'Name': 'CELTICS', 'TeamID': '1610612738'},
    'CLE': {'Name': 'CAVALIERS', 'TeamID': '1610612739'},
    'NOP': {'Name': 'PELICANS', 'TeamID': '1610612740'},

    'CHI': {'Name': 'BULLS', 'TeamID': '1610612741'},
    'DAL': {'Name': 'MAVERICKS', 'TeamID': '1610612742'},
    'DEN': {'Name': 'NUGGETS', 'TeamID': '1610612743'},
    'GSW': {'Name': 'WARRIORS', 'TeamID': '1610612744'},

    'HOU': {'Name': 'ROCKETS', 'TeamID': '1610612745'},
    'LAC': {'Name': 'CLIPPERS', 'TeamID': '1610612746'},
    'LAL': {'Name': 'LAKERS', 'TeamID': '1610612747'},
    'MIA': {'Name': 'HEAT', 'TeamID': '1610612748'},

    'MIL': {'Name': 'BUCKS', 'TeamID': '1610612749'},
    'MIN': {'Name': 'TIMBERWOLVES', 'TeamID': '1610612750'},
    'BKN': {'Name': 'NETS', 'TeamID': '1610612751'},
    'NYK': {'Name': 'KNICKS', 'TeamID': '1610612752'},

    'ORL': {'Name': 'MAGIC', 'TeamID': '1610612753'},
    'IND': {'Name': 'PACERS', 'TeamID': '1610612754'},
    'PHI': {'Name': '76ERS', 'TeamID': '1610612755'},
    'PHO': {'Name': 'SUNS', 'TeamID': '1610612756'},

    'POR': {'Name': 'TRAIL BLAZERS', 'TeamID': '1610612757'},
    'SAC': {'Name': 'KINGS', 'TeamID': '1610612758'},
    'SAS': {'Name': 'SPURS', 'TeamID': '1610612759'},
    'OKC': {'Name': 'THUNDER', 'TeamID': '1610612760'},

    'TOR': {'Name': 'RAPTORS', 'TeamID': '1610612761'},
    'UTA': {'Name': 'JAZZ', 'TeamID': '1610612762'},
    'MEM': {'Name': 'GRIZZLIES', 'TeamID': '1610612763'},
    'WAS': {'Name': 'WIZARDS', 'TeamID': '1610612764'},

    'DET': {'Name': 'PISTONS', 'TeamID': '1610612765'},
    'CHA': {'Name': 'HORNETS', 'TeamID': '1610612766'}

}


def getWeekIdx(date):
    for weekIdx, weekdate in WeekInfo.iteritems():
        if date in range(weekdate[0], weekdate[1] + 1):
            return weekIdx
    return None


def getAllTeamSchedules(yearSchedule):
    allTeamSchedules = {}
    for dateKey, gameSets in yearSchedule.iteritems():
        for gameID, gameInfo in gameSets.iteritems():
            hostID = gameInfo["CUSTOM_HOST"]
            if not allTeamSchedules.has_key(hostID):
                allTeamSchedules[hostID] = {}
            allTeamSchedules[hostID][dateKey] = gameInfo

            visitorID = gameInfo["CUSTOM_VISITOR"]
            if not allTeamSchedules.has_key(visitorID):
                allTeamSchedules[visitorID] = {}
            allTeamSchedules[visitorID][dateKey] = gameInfo
    return allTeamSchedules


def queryNBAData(url, params, session=None):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36', 
        'referer': 'https://stats.nba.com/',
        'host': 'data.nba.com',
        'connection':'keep-alive'
    }
    if session is not None:
        resp = session.get(url, headers=headers, params=params, verify=False)
    else:
        resp = requests.get(url, headers=headers, params=params, verify=False)
    return resp


def queryNBAStats(url, params, session=None):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36', 
        'referer': 'https://stats.nba.com/',
        'host': 'stats.nba.com',
        'connection':'keep-alive'
    }
    if session is not None:
        resp = session.get(url, headers=headers, params=params, verify=False)
        print resp.url
    else:
        resp = requests.get(url, headers=headers, params=params, verify=False)
    return resp


def queryBoxscoreTraditionalV2(gameID, filename, session=None, cache=False):
    if cache is False:
        url = "https://stats.nba.com/stats/boxscoretraditionalv2" 
        params = {
            "EndPeriod": "10",
            "EndRange": "28800",
            "GameID": gameID,
            "RangeType": "0",
            "StartPeriod": "1",
            "StartRange": "0"
            }
        resp = queryNBAStats(url, params, session=session)
        # print resp.text
        result = json.loads(resp.text)
        # print result
        resultSets = result["resultSets"]
        # print resultSets

        headers = []
        players = {}
        for resultSet in resultSets:
            if resultSet["name"] == "PlayerStats":
                headers = resultSet["headers"]
                for headerIdx, header in enumerate(headers):
                    if header == "PLAYER_ID":
                        playerIDIdx = headerIdx
                        for playerStats in resultSet["rowSet"]:
                            playerID = playerStats[playerIDIdx]
                            players[playerID] = {}
                            for statIdx, statValue in enumerate(playerStats):
                                players[playerID][headers[statIdx]] = statValue if statValue is not None else 0
        # print headers
        # print players

        with open(filename, "w+") as f:
            pickle.dump(players, f)

    else:
        with open(filename, "r") as f:
            players = pickle.load(f)

    return players


def queryNBATeamRoster(id, year, session=None):
    url = "https://stats.nba.com/stats/commonteamroster" 
    params = {
        "LeagueID": "00", 
        "Season": year, 
        "TeamID": str(id)
    }
    resp = queryNBAStats(url, params, session=session)
    # print resp.text
    result = json.loads(resp.text)
    # print result

    rosterResultSet = None
    for resultSet in result["resultSets"]:
        if resultSet["name"] == "CommonTeamRoster":
             rosterResultSet = resultSet
    # print rosterResultSet

    teamRoster = []
    for playerResultRow in rosterResultSet["rowSet"]:
        playerStat = {}
        for attrIdx, attr in enumerate(playerResultRow):
            playerStat[rosterResultSet["headers"][attrIdx]] = attr
        teamRoster.append(playerStat)
    # print teamRoster

    return teamRoster

def queryNBAPlayer(id, year, session=None):
    url = "https://stats.nba.com/stats/playerdashboardbyyearoveryear" 
    params = {
        "DateFrom": "",
        "DateTo": "",
        "GameSegment": "",
        "LastNGames": "0", 
        "LeagueID": "00", 
        "Location": "",
        "MeasureType": "Base", 
        "Month": "0", 
        "OpponentTeamID": "0", 
        "Outcome": "",
        "PORound": "0", 
        "PaceAdjust": "N", 
        "PerMode": "Totals", 
        "Period": "0", 
        "PlayerID": str(id), 
        "PlusMinus":"N", 
        "Rank": "N", 
        "Season": year, 
        "SeasonSegment": "",
        "SeasonType": "Regular Season", 
        "ShotClockRange": "",
        "Split":"yoy",
        "VsConference": "",
        "VsDivision": ""
        }
    resp = queryNBAStats(url, params, session=session)
    # print resp.text
    result = json.loads(resp.text)
    # print result

    byYearResultSet = None
    for resultSet in result["resultSets"]:
        if resultSet["name"] == "ByYearPlayerDashboard":
             byYearResultSet = resultSet
    # print byYearResultSet

    statsHeaders = byYearResultSet["headers"]
    # print statsHeaders

    yearStats = None
    for yearResultRow in byYearResultSet["rowSet"]:
        tmpYearStats = {}
        for attrIdx, attr in enumerate(yearResultRow):
            tmpYearStats[byYearResultSet["headers"][attrIdx]] = attr
        if tmpYearStats["GROUP_VALUE"] == year:
            yearStats = tmpYearStats
    # print yearStats

    if yearStats is None:
        yearStats = {}
        for header in statsHeaders:
            yearStats[header] = 0
    # print yearStats

    return yearStats


def queryLeaguePlayerStats(year, filename, session=None, cache=False):
    if cache is False:
        players = {}
        for teamAbbr, teamInfo in NBATeamInfo.iteritems():
            teamroster = queryNBATeamRoster(teamInfo["TeamID"], year, session=session)

            for playerinfo in teamroster:
                playerStats = queryNBAPlayer(playerinfo["PLAYER_ID"], year, session=session)
                playerinfo.update(playerStats)
                players[playerinfo["PLAYER_ID"]] = playerinfo

            time.sleep(1)

        with open(filename, "w+") as f:
            pickle.dump(players, f)

    else:
        with open(filename, "r") as f:
            players = pickle.load(f)

    return players


def queryPlayerDashboardByLastNGames(year, playerID, lastngames, session=None, cache=False):
    filename = "playerdashboardbylastngames_%s_%s.pickle" % (playerID, year)
    if cache is False:
        url = "https://stats.nba.com/stats/playerdashboardbylastngames" 
        params = {
            "DateFrom": "",
            "DateTo": "",
            "GameSegment": "",
            "LastNGames": "0", 
            "LeagueID": "00", 
            "Location": "",
            "MeasureType": "Base", 
            "Month": "0", 
            "OpponentTeamID": "0", 
            "Outcome": "",
            "PORound": "0", 
            "PaceAdjust": "N", 
            "PerMode": "Totals", 
            "Period": "0", 
            "PlayerID": str(playerID), 
            "PlusMinus":"N", 
            "Rank": "N", 
            "Season": year, 
            "SeasonSegment": "",
            "SeasonType": "Regular Season", 
            "ShotClockRange": "",
            "Split": "lastn",
            "VsConference": "",
            "VsDivision": ""
            }
        resp = queryNBAStats(url, params, session=session)
        # print resp.text
        result = json.loads(resp.text)
        # print result
        resultSets = result["resultSets"]
        # print resultSets
        with open(filename, "w+") as f:
            pickle.dump(resultSets, f)
        time.sleep(1)
    else:
        with open(filename, "r") as f:
            resultSets = pickle.load(f)
    # print resultSets

    requestResource = "Last%dPlayerDashboard" % lastngames
    # print requestResource
    headers = []
    playerStatsInfo = {}
    for resultSet in resultSets:
        # print resultSet["name"]
        if resultSet["name"] == requestResource:
            # print resultSet
            statsList = resultSet["headers"]
            # print statsList
            # print resultSet["rowSet"]
            # print len(resultSet["rowSet"])
            for statsIdx, stats in enumerate(statsList):
                if len(resultSet["rowSet"]) > 0:
                    playerStatsInfo[stats] = resultSet["rowSet"][0][statsIdx]
                else:
                    playerStatsInfo[stats] = 0
    # print headers
    # print playerStatsInfo

    return playerStatsInfo


def queryNBAPlayerRecentStatsInfo(playerInfo, year, lastngames=5, session=None, cache=False):
    playerStatsInfo = copy.deepcopy(playerInfo)
    # print playerStatsInfo
    playerID = playerStatsInfo["PLAYER_ID"]
    # print playerID
    tmpPlayerStatsInfo = queryPlayerDashboardByLastNGames(year, playerID, lastngames, session=session, cache=cache)
    # print json.dumps(tmpPlayerStatsInfo, indent=4, sort_keys=True)
    playerStatsInfo.update(tmpPlayerStatsInfo)
    # print json.dumps(playerStatsInfo, indent=4, sort_keys=True)
    return playerStatsInfo


def queryNBAPlayerInfoDict(year, session=None, cache=False):
    playerInfoDict = {}
    for teamID in NBATeamDict.keys():
        filename = "teamroster_%s_%s.pickle" % (teamID, year)
        if cache is False:
            teamroster = queryNBATeamRoster(teamID, year, session=session)
            for playerInfo in teamroster:
                playerInfoDict[playerInfo["PLAYER_ID"]] = playerInfo
            with open(filename, "w+") as f:
                pickle.dump(playerInfoDict, f)
            time.sleep(1)
        else:
            with open(filename, "r") as f:
                playerInfoDict = pickle.load(f)
    # print json.dumps(playerInfoDict, indent=4, sort_keys=True)

    for playerID in playerInfoDict:
        playerInfoDict[playerID]["PLAYER_NAME"] = playerInfoDict[playerID]["PLAYER"]
        # print playerInfoDict[playerID]["PLAYER"]
        playerInfoDict[playerID]["TEAM_ID"] = playerInfoDict[playerID]["TeamID"]
        # print playerInfoDict[playerID]["TeamID"]
        playerInfoDict[playerID]["TEAM_ABBREVIATION"] = NBATeamDict[str(playerInfoDict[playerID]["TeamID"])]["Abbreviation"]
        del playerInfoDict[playerID]["TeamID"]
        del playerInfoDict[playerID]["PLAYER"]
    # print json.dumps(playerInfoDict, indent=4, sort_keys=True)
    return playerInfoDict


def queryLeagueDashPlayerStats(year, filename, session=None, cache=False, lastngames=0):
    if cache is False:
        url = "https://stats.nba.com/stats/leaguedashplayerstats" 
        params = {
            "College": "",
            "Conference": "",
            "Country": "",
            "DateFrom": "",
            "DateTo": "",
            "Division": "",
            "DraftPick": "",
            "DraftYear": "",
            "GameScope": "",
            "GameSegment": "",
            "Height": "",
            "LastNGames": lastngames, 
            "LeagueID": "00", 
            "Location": "",
            "MeasureType": "Base", 
            "Month": "0", 
            "OpponentTeamID": "0", 
            "Outcome": "",
            "PORound": "0", 
            "PaceAdjust": "N", 
            "PerMode": "Totals", 
            "Period": "0", 
            "PlayerExperience": "", 
            "PlayerPosition": "", 
            "PlusMinus":"N", 
            "Rank": "N", 
            "Season": year, 
            "SeasonSegment": "",
            "SeasonType": "Regular Season", 
            "ShotClockRange": "",
            "StarterBench": "",
            "TeamID":"0",
            "VsConference": "",
            "VsDivision": "",
            "Weight": ""
            }
        resp = queryNBAStats(url, params, session=session)
        # print resp.text
        result = json.loads(resp.text)
        # print result
        resultSets = result["resultSets"]
        # print resultSets

        headers = []
        players = {}
        for resultSet in resultSets:
            if resultSet["name"] == "LeagueDashPlayerStats":
                headers = resultSet["headers"]
                for playerStats in resultSet["rowSet"]:
                    playerID = playerStats[0]
                    players[playerID] = {}
                    for statIdx, statValue in enumerate(playerStats):
                        players[playerID][headers[statIdx]] = statValue
        # print headers
        # print players

        with open(filename, "w+") as f:
            pickle.dump(players, f)

    else:
        with open(filename, "r") as f:
            players = pickle.load(f)

    return players


def queryNBAYearSchedule(year, filename, session=None, cache=False):
    if cache is False:
        url = "https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/%s/league/00_full_schedule_week.json" % year[0:4]
        resp = queryNBAData(url, None, session=session)
        # print resp.text
        result = json.loads(resp.text)
        # print result

        yearSchedule = {}
        for month in result["lscd"]:
            monthID = month["mscd"]["mon"]
            for game in month["mscd"]["g"]:
                gid = game["gid"]
                gcode = game["gcode"]
                date = gcode[0:8]
                visitor = gcode[9:12]
                host = gcode[12:15]
                game["CUSTOM_HOST"] = host
                game["CUSTOM_VISITOR"] = visitor
                if not yearSchedule.has_key(date):
                    yearSchedule[date] = {}
                yearSchedule[date][gid] = game

        # print yearSchedule

        with open(filename, "w+") as f:
            pickle.dump(yearSchedule, f)

    else:
        with open(filename, "r") as f:
            yearSchedule = pickle.load(f)

    return yearSchedule


def writeAllPlayerStats2CSV(headers, allPlayerStats, filename):
    statHeaders = copy.deepcopy(headers)

    with open(filename, "wb+") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';')

        statHeaders.sort()
        print statHeaders

        for exemptHeader in ["EXP", "GROUP_SET", "GROUP_VALUE", "HEIGHT", "LeagueID", "MAX_GAME_DATE", "NUM", "BIRTH_DATE", "PLAYER", "POSITION", "SEASON", "SCHOOL"]:
            if exemptHeader in statHeaders:
                statHeaders.remove(exemptHeader)
        print statHeaders

        statHeaders.remove("PLAYER_NAME")
        statHeaders.remove("PLAYER_ID")
        statHeaders.insert(0, "PLAYER_ID")
        spamwriter.writerow(["PLAYER_NAME", 1] + statHeaders)

        spamwriter.writerow([(i+1) for i in range(0, len(statHeaders) + 2)])

        allPlayerInfo = {}
        for playerID, playerStats in allPlayerStats.iteritems():
            # print playerStats
            playerName = playerStats["PLAYER_NAME"]
            if not allPlayerInfo.has_key(playerName):
                allPlayerInfo[playerName] = []
            allPlayerInfo[playerName].append(playerID)
            allPlayerInfo[playerName].sort()
        # print allPlayerInfo

        allPlayerNames = allPlayerInfo.keys()
        allPlayerNames.sort()
        # print allPlayerNames

        for playerCnt, playerName in enumerate(allPlayerNames):
            for playerID in allPlayerInfo[playerName]:
                cells = [playerName, (playerCnt + 3)] + [allPlayerStats[playerID][statHeader] for statHeader in statHeaders]
                spamwriter.writerow(cells)

def getStatsHeaders(allPlayerStats):
    for playerID in allPlayerStats:
        return allPlayerStats[playerID].keys()
    return []

def generateAllPlayerStats(partPlayerStats, baseAllPlayerStats):
    baseAllPlayerStatsHeaders = getStatsHeaders(baseAllPlayerStats)
    # print baseAllPlayerStatsHeaders

    newAllPlayerStats = {}
    for playerID, playerStats in baseAllPlayerStats.iteritems():
        newAllPlayerStats[playerID] = {}
        for statKey in baseAllPlayerStatsHeaders:
            if statKey in ["PLAYER_ID", "PLAYER_NAME"]:
                newAllPlayerStats[playerID][statKey] = baseAllPlayerStats[playerID][statKey]
            elif partPlayerStats.has_key(playerID) and partPlayerStats[playerID].has_key(statKey):
                newAllPlayerStats[playerID][statKey] = partPlayerStats[playerID][statKey]
            else:
                newAllPlayerStats[playerID][statKey] = 0
    return newAllPlayerStats


# if __name__ == "__main__":
#     year = "2017-18"

#     with requests.Session() as s:

#         allPlayerStats = queryLeaguePlayerStats(year, "leagueplayerstats_%s.pickle" % (year), session=s, cache=True)
#         # print json.dumps(allPlayerStats, indent=4, sort_keys=True)
#         for playerID in allPlayerStats:
#             allPlayerStats[playerID]["PLAYER_NAME"] = allPlayerStats[playerID]["PLAYER"]
#             del allPlayerStats[playerID]["PLAYER"]
#         # print json.dumps(allPlayerStats, indent=4, sort_keys=True)
#         allPlayerStatsHeaders = getStatsHeaders(allPlayerStats)
#         # print allPlayerStatsHeaders
#         writeAllPlayerStats2CSV(allPlayerStatsHeaders, allPlayerStats, "player_seasonal_stats_%s.csv" % (year))

#         yearSchedule = queryNBAYearSchedule(year, "full_schedule_%s.pickle" % (year), session=s, cache=False)
#         # print json.dumps(yearSchedule, indent=4, sort_keys=True)
#         allTeamSchedules = getAllTeamSchedules(yearSchedule)
#         # print json.dumps(allTeamSchedules, indent=4, sort_keys=True)
#         allPlayerSchedules = {}
#         for playerID, playerStats in allPlayerStats.iteritems():
#             allPlayerSchedules[playerID] = {"PLAYER_ID": playerID, "PLAYER_NAME": playerStats["PLAYER_NAME"]}
#             # print "playername: ", playerStats["PLAYER_NAME"]
#             teamAbbr = playerStats["TEAM_ABBREVIATION"]
#             # print "teamAbbr: ", teamAbbr
#             datefrom = datetime.datetime(2017, 10, 17)
#             dateto = datetime.datetime(2018, 04, 11)
#             while datefrom <= dateto:
#                 dateKey = datefrom.strftime("%Y%m%d")
#                 dateHeader = datefrom.strftime("%Y/%m/%d")
#                 # print "dateKey: ", dateKey
#                 if allTeamSchedules.has_key(teamAbbr) and allTeamSchedules[teamAbbr].has_key(dateKey):
#                     allPlayerSchedules[playerID][dateHeader] = 1
#                 else:
#                     allPlayerSchedules[playerID][dateHeader] = 0
#                 datefrom = datefrom + datetime.timedelta(days=1)
#         # print json.dumps(allPlayerSchedules, indent=4, sort_keys=True)
#         allPlayerSchedulesHeaders = getStatsHeaders(allPlayerSchedules)
#         # print allPlayerSchedulesHeaders
#         writeAllPlayerStats2CSV(allPlayerSchedulesHeaders, allPlayerSchedules, "player_schedule_%s.csv" % (year))

#         tmpAllPlayerLastNGamesStats = queryLeagueDashPlayerStats(year, "leaguedashplayerstats_%s_lastngames.pickle" % (year), session=s, lastngames=5, cache=False)
#         # print json.dumps(tmpAllPlayerLastNGamesStats, indent=4, sort_keys=True)
#         allPlayerLastNGamesStats = generateAllPlayerStats(tmpAllPlayerLastNGamesStats, allPlayerStats)
#         # print json.dumps(allPlayerLastNGamesStats, indent=4, sort_keys=True)
#         writeAllPlayerStats2CSV(allPlayerStatsHeaders, allPlayerLastNGamesStats, "player_lastngames_stats_%s.csv" % (year))



NBATeamDict = {
    
    '1610612737': {'Abbreviation': 'ATL', 'Name': 'HAWKS', 'TeamID': '1610612737'},
    '1610612738': {'Abbreviation': 'BOS', 'Name': 'CELTICS', 'TeamID': '1610612738'},
    '1610612739': {'Abbreviation': 'CLE', 'Name': 'CAVALIERS', 'TeamID': '1610612739'},
    '1610612740': {'Abbreviation': 'NOP', 'Name': 'PELICANS', 'TeamID': '1610612740'},

    '1610612741': {'Abbreviation': 'CHI', 'Name': 'BULLS', 'TeamID': '1610612741'},
    '1610612742': {'Abbreviation': 'DAL', 'Name': 'MAVERICKS', 'TeamID': '1610612742'},
    '1610612743': {'Abbreviation': 'DEN', 'Name': 'NUGGETS', 'TeamID': '1610612743'},
    '1610612744': {'Abbreviation': 'GSW', 'Name': 'WARRIORS', 'TeamID': '1610612744'},

    '1610612745': {'Abbreviation': 'HOU', 'Name': 'ROCKETS', 'TeamID': '1610612745'},
    '1610612746': {'Abbreviation': 'LAC', 'Name': 'CLIPPERS', 'TeamID': '1610612746'},
    '1610612747': {'Abbreviation': 'LAL', 'Name': 'LAKERS', 'TeamID': '1610612747'},
    '1610612748': {'Abbreviation': 'MIA', 'Name': 'HEAT', 'TeamID': '1610612748'},

    '1610612749': {'Abbreviation': 'MIL', 'Name': 'BUCKS', 'TeamID': '1610612749'},
    '1610612750': {'Abbreviation': 'MIN', 'Name': 'TIMBERWOLVES', 'TeamID': '1610612750'},
    '1610612751': {'Abbreviation': 'BKN', 'Name': 'NETS', 'TeamID': '1610612751'},
    '1610612752': {'Abbreviation': 'NYK', 'Name': 'KNICKS', 'TeamID': '1610612752'},

    '1610612753': {'Abbreviation': 'ORL', 'Name': 'MAGIC', 'TeamID': '1610612753'},
    '1610612754': {'Abbreviation': 'IND', 'Name': 'PACERS', 'TeamID': '1610612754'},
    '1610612755': {'Abbreviation': 'PHI', 'Name': '76ERS', 'TeamID': '1610612755'},
    '1610612756': {'Abbreviation': 'PHX', 'Name': 'SUNS', 'TeamID': '1610612756'},

    '1610612757': {'Abbreviation': 'POR', 'Name': 'TRAIL BLAZERS', 'TeamID': '1610612757'},
    '1610612758': {'Abbreviation': 'SAC', 'Name': 'KINGS', 'TeamID': '1610612758'},
    '1610612759': {'Abbreviation': 'SAS', 'Name': 'SPURS', 'TeamID': '1610612759'},
    '1610612760': {'Abbreviation': 'OKC', 'Name': 'THUNDER', 'TeamID': '1610612760'},

    '1610612761': {'Abbreviation': 'TOR', 'Name': 'RAPTORS', 'TeamID': '1610612761'},
    '1610612762': {'Abbreviation': 'UTA', 'Name': 'JAZZ', 'TeamID': '1610612762'},
    '1610612763': {'Abbreviation': 'MEM', 'Name': 'GRIZZLIES', 'TeamID': '1610612763'},
    '1610612764': {'Abbreviation': 'WAS', 'Name': 'WIZARDS', 'TeamID': '1610612764'},

    '1610612765': {'Abbreviation': 'DET', 'Name': 'PISTONS', 'TeamID': '1610612765'},
    '1610612766': {'Abbreviation': 'CHA', 'Name': 'HORNETS', 'TeamID': '1610612766'}

}



"""
TODO: Fetch from the yahoo fantasy website
"""
def fetchYahooFantasyLeagueInfo():
    NAN_ROSTER = [
        {"name":"Chris Paul", "team":"HOU", "position": ["PG","SG"]},
        {"name":"Buddy Hield", "team":"SAC", "position": ["PG","SG"]},
        {"name":"JJ Redick", "team":"PHI", "position": ["SG","SF"]},
        {"name":"Taurean Prince", "team":"ATL", "position": ["SF","PF"]},
        {"name":"Joel Embiid", "team":"PHI", "position": ["SF","PF"]},
        {"name":"Dirk Nowitzki", "team":"DAL", "position": ["PG","SG","SF"]},
        {"name":"Steven Adams", "team":"OKC", "position": ["PF","C"]},
        {"name":"Karl-Anthony Towns", "team":"MIN", "position": ["C"]},
        {"name":"Jordan Clarkson", "team":"LAL", "position": ["SG","SF"]},
        {"name":"Bobby Portis", "team":"CHI", "position": ["PG","SF","PF"]},
        {"name":"DeMar DeRozan", "team":"TOR", "position": ["SG","SF"]},
        {"name":"Donovan Mitchell", "team":"UTA", "position": ["SG","SF"]}
    ]

    SUHOW_ROSTER = [
        {"name":"Lonzo Ball", "team":"LAL", "position": ["PG","SG"]},
        {"name":"Bradley Beal", "team":"WAS", "position": ["PG","SG"]},
        {"name":"Devin Booker", "team":"PHX", "position": ["SG","SF"]},
        {"name":"Paul George", "team":"OKC", "position": ["SF","PF"]},
        {"name":"Nikola Vucevic", "team":"ORL", "position": ["SF","PF"]},
        {"name":"Clint Capela", "team":"HOU", "position": ["PG","SG","SF"]},
        {"name":"Robin Lopez", "team":"CHI", "position": ["PF","C"]},
        {"name":"Pau Gasol", "team":"SAS", "position": ["C"]},
        {"name":"Rudy Gay", "team":"SAS", "position": ["SG","SF"]},
        {"name":"Marcin Gortat", "team":"WAS", "position": ["PG","SF","PF"]},
        {"name":"Damian Lillard", "team":"POR", "position": ["SG","SF"]}
    ]

    PETER_ROSTER = [
        {"name":"Kemba Walker", "team":"CHA", "position": ["PG","SG"]},
        {"name":"Kent Bazemore", "team":"ATL", "position": ["PG","SG"]},
        {"name":"Kentavious Caldwell-Pope", "team":"LAL", "position": ["SG","SF"]},
        {"name":"TJ Warren", "team":"PHX", "position": ["SF","PF"]},
        {"name":"James Johnson", "team":"MIA", "position": ["SF","PF"]},
        {"name":"Kyle Kuzma", "team":"LAL", "position": ["PG","SG","SF"]},
        {"name":"Marquese Chriss", "team":"PHX", "position": ["PF","C"]},
        {"name":"Draymond Green", "team":"GSW", "position": ["C"]},
        {"name":"Will Barton", "team":"DEN", "position": ["SG","SF"]},
        {"name":"Austin Rivers", "team":"LAC", "position": ["PG","SF","PF"]},
        {"name":"Mike Conley", "team":"MEM", "position": ["SG","SF"]},
        {"name":"Jimmy Butler", "team":"MIN", "position": ["SG","SF"]}
    ]

    SHAWHAN_ROSTER = [
        {"name":"Kyrie Irving", "team":"BOS", "position": ["PG","SG"]},
        {"name":"D'Angelo Russell", "team":"BKN", "position": ["PG","SG"]},
        {"name":"Eric Gordon", "team":"HOU", "position": ["SG","SF"]},
        {"name":"Aaron Gordon", "team":"ORL", "position": ["SF","PF"]},
        {"name":"Andre Drummond", "team":"DET", "position": ["SF","PF"]},
        {"name":"Tim Hardaway Jr.", "team":"NYK", "position": ["PG","SG","SF"]},
        {"name":"Rudy Gobert", "team":"UTA", "position": ["PF","C"]},
        {"name":"Enes Kanter", "team":"NYK", "position": ["C"]},
        {"name":"Darren Collison", "team":"IND", "position": ["SG","SF"]},
        {"name":"Evan Fournier", "team":"ORL", "position": ["PG","SF","PF"]},
        {"name":"Julius Randle", "team":"LAL", "position": ["SG","SF"]},
        {"name":"Elfrid Payton", "team":"ORL", "position": ["SG","SF"]}
    ]

    DANNYKAO_ROSTER = [
        {"name":"Jerryd Bayless", "team":"PHI", "position": ["PG","SG"]},
        {"name":"Kelly Oubre Jr.", "team":"WAS", "position": ["PG","SG"]},
        {"name":"Jrue Holiday", "team":"NOP", "position": ["SG","SF"]},
        {"name":"Rondae Hollis-Jefferson", "team":"BKN", "position": ["SF","PF"]},
        {"name":"DeMarre Carroll", "team":"BKN", "position": ["SF","PF"]},
        {"name":"Brandon Ingram", "team":"LAL", "position": ["PG","SG","SF"]},
        {"name":"Nikola Jokic", "team":"DEN", "position": ["PF","C"]},
        {"name":"Kristaps Porzingis", "team":"NYK", "position": ["C"]},
        {"name":"Derrick Rose", "team":"CLE", "position": ["SG","SF"]},
        {"name":"LaMarcus Aldridge", "team":"SAS", "position": ["PG","SF","PF"]},
        {"name":"Dion Waiters", "team":"MIA", "position": ["SG","SF"]},
        {"name":"Evan Turner", "team":"POR", "position": ["SG","SF"]}
    ]

    CHINGCHUAN_ROSTER = [
        {"name":"Kyle Lowry", "team":"TOR", "position": ["PG","SG"]},
        {"name":"Lou Williams", "team":"LAC", "position": ["PG","SG"]},
        {"name":"Spencer Dinwiddie", "team":"BKN", "position": ["SG","SF"]},
        {"name":"Andrew Wiggins", "team":"MIN", "position": ["SF","PF"]},
        {"name":"Anthony Davis", "team":"NOP", "position": ["SF","PF"]},
        {"name":"Carmelo Anthony", "team":"OKC", "position": ["PG","SG","SF"]},
        {"name":"Jayson Tatum", "team":"BOS", "position": ["PF","C"]},
        {"name":"Jonas Valanciunas", "team":"TOR", "position": ["C"]},
        {"name":"Willie Cauley-Stein", "team":"SAC", "position": ["SG","SF"]},
        {"name":"Ryan Anderson", "team":"HOU", "position": ["PG","SF","PF"]},
        {"name":"Dennis Schroder", "team":"ATL", "position": ["SG","SF"]},
        {"name":"Bojan Bogdanovic", "team":"IND", "position": ["SG","SF"]}
    ]

    SUDEELER_ROSTER = [
        {"name":"John Wall", "team":"WAS", "position": ["PG","SG"]},
        {"name":"George Hill", "team":"SAC", "position": ["PG","SG"]},
        {"name":"Mike James", "team":"PHX", "position": ["SG","SF"]},
        {"name":"Kevin Durant", "team":"GSW", "position": ["SF","PF"]},
        {"name":"Marcus Morris", "team":"BOS", "position": ["SF","PF"]},
        {"name":"Dario Saric", "team":"PHI", "position": ["PG","SG","SF"]},
        {"name":"Hassan Whiteside", "team":"MIA", "position": ["PF","C"]},
        {"name":"Kelly Olynyk", "team":"MIA", "position": ["C"]},
        {"name":"Reggie Jackson", "team":"DET", "position": ["SG","SF"]},
        {"name":"Terry Rozier", "team":"BOS", "position": ["PG","SF","PF"]},
        {"name":"Jae Crowder", "team":"UTA", "position": ["SG","SF"]},
        {"name":"Joe Ingles", "team":"CLE", "position": ["SG","SF"]}
    ]

    ANBHDY_ROSTER = [
        {"name":"Dennis Smith Jr.", "team":"DAL", "position": ["PG","SG"]},
        {"name":"Klay Thompson", "team":"GSW", "position": ["PG","SG"]},
        {"name":"Marcus Smart", "team":"BOS", "position": ["SG","SF"]},
        {"name":"Gary Harris", "team":"DEN", "position": ["SF","PF"]},
        {"name":"Robert Covington", "team":"PHI", "position": ["SF","PF"]},
        {"name":"Tyreke Evans", "team":"MEM", "position": ["PG","SG","SF"]},
        {"name":"Jusuf Nurkic", "team":"POR", "position": ["PF","C"]},
        {"name":"John Collins", "team":"ATL", "position": ["C"]},
        {"name":"Harrison Barnes", "team":"DAL", "position": ["SG","SF"]},
        {"name":"Thaddeus Young", "team":"IND", "position": ["PG","SF","PF"]},
        {"name":"Stephen Curry", "team":"GSW", "position": ["SG","SF"]},
        {"name":"Blake Griffin", "team":"LAC", "position": ["SG","SF"]}
    ]

    ABELHUANG_ROSTER = [
        {"name":"Jeff Teague", "team":"MIN", "position": ["PG","SG"]},
        {"name":"James Harden", "team":"HOU", "position": ["PG","SG"]},
        {"name":"Ricky Rubio", "team":"UTA", "position": ["SG","SF"]},
        {"name":"Tobias Harris", "team":"DET", "position": ["SF","PF"]},
        {"name":"Domantas Sabonis", "team":"IND", "position": ["SF","PF"]},
        {"name":"Danilo Gallinari", "team":"LAC", "position": ["PG","SG","SF"]},
        {"name":"Kevin Love", "team":"CLE", "position": ["PF","C"]},
        {"name":"Serge Ibaka", "team":"TOR", "position": ["C"]},
        {"name":"Brook Lopez", "team":"LAL", "position": ["SG","SF"]},
        {"name":"Lauri Markkanen", "team":"CHI", "position": ["PG","SF","PF"]},
        {"name":"Victor Oladipo", "team":"IND", "position": ["SG","SF"]},
        {"name":"Jaylen Brown", "team":"BOS", "position": ["SG","SF"]}
    ]

    YUAN_ROSTER = [
        {"name":"Russell Westbrook", "team":"OKC", "position": ["PG","SG"]},
        {"name":"Kyle Korver", "team":"CLE", "position": ["PG","SG"]},
        {"name":"Allen Crabbe", "team":"BKN", "position": ["SG","SF"]},
        {"name":"Trevor Ariza", "team":"HOU", "position": ["SF","PF"]},
        {"name":"LeBron James", "team":"CLE", "position": ["SF","PF"]},
        {"name":"Taj Gibson", "team":"MIN", "position": ["PG","SG","SF"]},
        {"name":"Danny Green", "team":"SAS", "position": ["PF","C"]},
        {"name":"Kyle O'Quinn", "team":"NYK", "position": ["C"]},
        {"name":"Zach Randolph", "team":"SAC", "position": ["SG","SF"]},
        {"name":"Marco Belinelli", "team":"ATL", "position": ["PG","SF","PF"]},
        {"name":"CJ McCollum", "team":"POR", "position": ["SG","SF"]},
        {"name":"Avery Bradley", "team":"DET", "position": ["SG","SF"]}
    ]

    CHIYU_ROSTER = [
        {"name":"Patrick Beverley", "team":"LAC", "position": ["PG","SG"]},
        {"name":"Dwyane Wade", "team":"CLE", "position": ["PG","SG"]},
        {"name":"Justin Holiday", "team":"CHI", "position": ["SG","SF"]},
        {"name":"Otto Porter Jr.", "team":"WAS", "position": ["SF","PF"]},
        {"name":"Giannis Antetokounmpo", "team":"MIL", "position": ["SF","PF"]},
        {"name":"Kris Dunn", "team":"CHI", "position": ["PG","SG","SF"]},
        {"name":"DeMarcus Cousins", "team":"NOP", "position": ["PF","C"]},
        {"name":"Dewayne Dedmon", "team":"ATL", "position": ["C"]},
        {"name":"Jeremy Lamb", "team":"CHA", "position": ["SG","SF"]},
        {"name":"Ben Simmons", "team":"PHI", "position": ["PG","SF","PF"]},
        {"name":"Wesley Matthews", "team":"DAL", "position": ["SG","SF"]},
        {"name":"Denzel Valentine", "team":"CHI", "position": ["SG","SF"]}
    ]

    MARK_ROSTER = [
        {"name":"Malcolm Brogdon", "team":"MIL", "position": ["PG","SG"]},
        {"name":"Myles Turner", "team":"IND", "position": ["PG","SG"]},
        {"name":"J.J. Barea", "team":"DAL", "position": ["SG","SF"]},
        {"name":"Khris Middleton", "team":"MIL", "position": ["SF","PF"]},
        {"name":"Al Horford", "team":"BOS", "position": ["SF","PF"]},
        {"name":"DeAndre Jordan", "team":"LAC", "position": ["PG","SG","SF"]},
        {"name":"Dwight Howard", "team":"CHA", "position": ["PF","C"]},
        {"name":"Paul Millsap", "team":"DEN", "position": ["C"]},
        {"name":"Goran Dragic", "team":"MIA", "position": ["SG","SF"]},
        {"name":"Marc Gasol", "team":"MEM", "position": ["PG","SF","PF"]},
        {"name":"Eric Bledsoe", "team":"MIL", "position": ["SG","SF"]},
        {"name":"Rodney Hood", "team":"UTA", "position": ["SG","SF"]}
    ]

    teams = [
        {"name": "NAN", "roster":NAN_ROSTER},
        {"name": "SUHOW", "roster":SUHOW_ROSTER},
        {"name": "PETER", "roster":PETER_ROSTER},
        {"name": "SHAWHAN", "roster":SHAWHAN_ROSTER},
        {"name": "DANNYKAO", "roster":DANNYKAO_ROSTER},
        {"name": "CHINGCHUAN", "roster":CHINGCHUAN_ROSTER},
        {"name": "SUDEELER", "roster":SUDEELER_ROSTER},
        {"name": "ANBHDY", "roster":ANBHDY_ROSTER},
        {"name": "ABELHUANG", "roster":ABELHUANG_ROSTER},
        {"name": "YUAN", "roster":YUAN_ROSTER},
        {"name": "CHIYU", "roster":CHIYU_ROSTER, "matchup": ["NAN", "SUDEELER", "MARK", "ANBHDY", "SUHOW", "YUAN", "SHAWHAN", "DANNYKAO", "CHINGCHUAN", "PETER", "ABELHUANG", "NAN", "SUDEELER", "MARK", "ANBHDY", "SUHOW", "YUAN", "SHAWHAN", "DANNYKAO", "CHINGCHUAN", "", "", "", "", ""]},
        {"name": "MARK", "roster":MARK_ROSTER}
    ]

    # teams = [
    #     {"name": "CHIYU", "roster":CHIYU_ROSTER, "rosterMatrix":None, "matchup": ["NAN", "SUDEELER", "MARK", "ANBHDY", "SUHOW", "YUAN", "SHAWHAN", "DANNYKAO", "CHINGCHUAN", "PETER", "ABELHUANG", "NAN", "SUDEELER", "MARK", "ANBHDY", "SUHOW", "YUAN", "SHAWHAN", "DANNYKAO", "CHINGCHUAN"]}
    # ]

    leagueInfo = {
        "teams": teams,
        "items": ["FGM", "FGA", "FTM", "FTA", "FG3M", "FG3A", "PTS", "REB", "AST", "STL", "BLK", "TOV", "DD2"]
    }
    
    return leagueInfo

class Matrix:

    @staticmethod
    def Add(matrixA, matrixB):

        if not isinstance(matrixA[0], list):
            matrixA = [matrixA]
        if not isinstance(matrixB[0], list):
            matrixB = [matrixB]

        matrix = []
        for row in range(0, len(matrixA)):
            # print "row:", row
            subMatrix = []
            for col in range(0, len(matrixA[row])):
                # print "col:", col
                subMatrix.append(matrixA[row][col] + matrixB[row][col])
            matrix.append(subMatrix)

        if len(matrix) == 1:
            if len(matrix[0]) == 1:
                return matrix[0][0]
            else:
                return matrix[0]
        else:
            return matrix

    @staticmethod
    def Subtract(matrixA, matrixB):

        if not isinstance(matrixA[0], list):
            matrixA = [matrixA]
        if not isinstance(matrixB[0], list):
            matrixB = [matrixB]

        matrix = []
        for row in range(0, len(matrixA)):
            # print "row:", row
            subMatrix = []
            for col in range(0, len(matrixA[row])):
                # print "col:", col
                # print "matrixA[row][col]:", matrixA[row][col]
                # print "matrixB[row][col]:", matrixB[row][col]
                # print "matrixA[row][col] - matrixB[row][col]:", (matrixA[row][col] - matrixB[row][col])
                subMatrix.append(matrixA[row][col] - matrixB[row][col])
            matrix.append(subMatrix)

        if len(matrix) == 1:
            if len(matrix[0]) == 1:
                return matrix[0][0]
            else:
                return matrix[0]
        else:
            return matrix

    @staticmethod
    def And(matrixA, matrixB):

        if not isinstance(matrixA[0], list):
            matrixA = [matrixA]
        if not isinstance(matrixB[0], list):
            matrixB = [matrixB]

        matrix = []
        for row in range(0, len(matrixA)):
            # print "row:", row
            subMatrix = []
            for col in range(0, len(matrixA[row])):
                # print "col:", col
                if matrixA[row][col] == 1 and matrixB[row][col] == 1:
                    subMatrix.append(1)
                else:
                    subMatrix.append(0)
            matrix.append(subMatrix)

        if len(matrix) == 1:
            if len(matrix[0]) == 1:
                return matrix[0][0]
            else:
                return matrix[0]
        else:
            return matrix

    @staticmethod
    def Transpose(matrixA):
        if not isinstance(matrixA[0], list):
            matrixA = [matrixA]

        row = 0
        col = 0
        # print len(matrixA[0])
        # print len(matrixA)
        matrix = []
        for col in range(0, len(matrixA[0])):
            # print "col:", col
            subMatrix = []
            for row in range(0, len(matrixA)):
                # print "row:", row
                subMatrix.append(matrixA[row][col])
            matrix.append(subMatrix)

        if len(matrix) == 1:
            if len(matrix[0]) == 1:
                return matrix[0][0]
            else:
                return matrix[0]
        else:
            return matrix

    @staticmethod
    def Cross(matrixA, matrixB):
        if not isinstance(matrixA[0], list):
            matrixA = [matrixA]
        if not isinstance(matrixB[0], list):
            matrixB = [matrixB]

        matrix = []
        for arow in range(0, len(matrixA)):
            # print "arow:", arow
            subMatrix = []
            for bcol in range(0, len(matrixB[0])):
                # print "bcol:", bcol
                sumup = 0
                for acol in range(0, len(matrixA[arow])):
                    # print "acol:", acol 
                    # print "matrixA[%d][%d] = %d" % (arow, acol, matrixA[arow][acol])
                    brow = acol
                    # print "brow:", brow
                    # print "matrixB[%d][%d] = %d" % (brow, bcol, matrixB[brow][bcol])
                    sumup = sumup + matrixA[arow][acol] * matrixB[brow][bcol]
                subMatrix.append(sumup)
            matrix.append(subMatrix)

        if len(matrix) == 1:
            if len(matrix[0]) == 1:
                return matrix[0][0]
            else:
                return matrix[0]
        else:
            return matrix

WeekInfoList = [
    (datetime.datetime(2017,10,17), datetime.datetime(2017,10,22)),
    (datetime.datetime(2017,10,23), datetime.datetime(2017,10,29)),
    (datetime.datetime(2017,10,30), datetime.datetime(2017,11,5)),
    (datetime.datetime(2017,11,6), datetime.datetime(2017,11,12)),
    (datetime.datetime(2017,11,13), datetime.datetime(2017,11,19)),
    (datetime.datetime(2017,11,20), datetime.datetime(2017,11,26)),
    (datetime.datetime(2017,11,27), datetime.datetime(2017,12,3)),
    (datetime.datetime(2017,12,4), datetime.datetime(2017,12,10)),
    (datetime.datetime(2017,12,11), datetime.datetime(2017,12,17)),
    (datetime.datetime(2017,12,18), datetime.datetime(2017,12,24)),
    (datetime.datetime(2017,12,25), datetime.datetime(2017,12,31)),
    (datetime.datetime(2018,1,1), datetime.datetime(2018,1,7)),
    (datetime.datetime(2018,1,8), datetime.datetime(2018,1,14)),
    (datetime.datetime(2018,1,15), datetime.datetime(2018,1,21)),
    (datetime.datetime(2018,1,22), datetime.datetime(2018,1,28)),
    (datetime.datetime(2018,1,29), datetime.datetime(2018,2,4)),
    (datetime.datetime(2018,2,5), datetime.datetime(2018,2,11)),
    (datetime.datetime(2018,2,12), datetime.datetime(2018,2,25)),
    (datetime.datetime(2018,2,26), datetime.datetime(2018,3,4)),
    (datetime.datetime(2018,3,5), datetime.datetime(2018,3,11)),
    (datetime.datetime(2018,3,12), datetime.datetime(2018,3,18)),
    (datetime.datetime(2018,3,19), datetime.datetime(2018,3,25)),
    (datetime.datetime(2018,3,26), datetime.datetime(2018,4,1)),
    (datetime.datetime(2018,4,2), datetime.datetime(2018,4,8)),
    (datetime.datetime(2018,4,9), datetime.datetime(2018,4,11))
]


def getDates2WeeksMatrix(weekList):
    weekMatrix = []
    for (wdatefrom, wdateto) in weekList:
        daysVector = []
        datefrom = datetime.datetime(2017, 10, 17)
        dateto = datetime.datetime(2018, 4, 11)
        datenow = datefrom
        while datenow <= dateto:
            if datenow >= wdatefrom and datenow <= wdateto:
                daysVector.append(1)
            else:
                daysVector.append(0)
            datenow = datenow + datetime.timedelta(days=1)
        weekMatrix.append(daysVector)
    return weekMatrix


def getNBATeamScheduledDatesVector(teamID, allTeamSchedules):
    nbaTeamScheduledDatesVector = []
    datefrom = datetime.datetime(2017, 10, 17)
    dateto = datetime.datetime(2018, 4, 11)
    datenow = datefrom
    while datenow <= dateto:
        datekey = datenow.strftime("%Y%m%d")
        if allTeamSchedules[teamID].has_key(datekey):
            nbaTeamScheduledDatesVector.append(1)
        else:
            nbaTeamScheduledDatesVector.append(0)
        datenow = datenow + datetime.timedelta(days=1)
    return nbaTeamScheduledDatesVector


def getAllNBATeamScheduledWeeksVector(weekInfoList, allNBATeamSchedules):
    allNBATeamScheduledWeeksVectorDict = {}
    dates2weeksMatrix = getDates2WeeksMatrix(weekInfoList)
    # print dates2weeksMatrix
    # print len(dates2weeksMatrix)
    # print len(dates2weeksMatrix[0])
    for teamID in NBATeamDict.keys():
        # print teamID
        teamAbbr = NBATeamDict[teamID]["Abbreviation"]
        nbaTeamScheduledDatesVector = Matrix.Transpose(getNBATeamScheduledDatesVector(teamAbbr, allNBATeamSchedules))
        # print nbaTeamScheduledDatesVector
        # print len(nbaTeamScheduledDatesVector)
        # print len(nbaTeamScheduledDatesVector[0])
        nbaTeamScheduledWeeksVector = Matrix.Cross(dates2weeksMatrix, nbaTeamScheduledDatesVector)
        # print nbaTeamScheduledWeeksVector
        # print len(nbaTeamScheduledWeeksVector)
        # print len(nbaTeamScheduledWeeksVector[0])
        allNBATeamScheduledWeeksVectorDict[teamAbbr] = Matrix.Transpose(nbaTeamScheduledWeeksVector)
    return allNBATeamScheduledWeeksVectorDict


def isMatchupWinned(matchupResultVector):
    winItems = 0
    for item in matchupResultVector:
        if item > 0:
            winItems = winItems + 1
        elif item < 0:
            winItems = winItems - 1
        else:
            winItems = winItems
    # print winItems
    return (winItems > 0)


def getMatchupResultWinnedWeeks(weeklyMatchupResultMatrix, weekFrom, weekTo):
    weekFromIdx = weekFrom - 1
    weekToIdx = weekTo - 1
    winWeeks = 0
    # print weeklyMatchupResultMatrix
    for weekIdx in range(weekFromIdx, weekToIdx + 1):
        weekMatchupResultVecotr = weeklyMatchupResultMatrix[weekIdx]
        # print weekMatchupResultVecotr
        if isMatchupWinned(weekMatchupResultVecotr) is True:
            winWeeks = winWeeks + 1
    # print winWeeks
    return winWeeks


def statsVector2matchupVector(statsVector):
    # in the order of ["FGM", "FGA", "FTM", "FTA", "FG3M", "FG3A", "PTS", "REB", "AST", "STL", "BLK", "TOV", "DD2"]
    matchupVector = []
    matchupVector.append(float(statsVector[0])/float(statsVector[1]) if statsVector[1] > 0 else float(0))
    matchupVector.append(float(statsVector[2])/float(statsVector[3]) if statsVector[3] > 0 else float(0))
    matchupVector.append(float(statsVector[4]))
    matchupVector.append(float(statsVector[4])/float(statsVector[5]) if statsVector[5] > 0 else float(0))
    matchupVector.append(float(statsVector[6]))
    matchupVector.append(float(statsVector[7]))
    matchupVector.append(float(statsVector[8]))
    matchupVector.append(float(statsVector[9]))
    matchupVector.append(float(statsVector[10]))
    matchupVector.append(float(0) - float(statsVector[11]))
    matchupVector.append(float(statsVector[12]))
    return matchupVector


def statsMatrix2matchupMatrix(statsMatrix):
    matchupMatrix = []
    for statsVector in statsMatrix:
        # print statsVector
        matchupVector = statsVector2matchupVector(statsVector)
        # print matchupVector
        matchupMatrix.append(matchupVector)
    return matchupMatrix


"""
Generate a matrix for selected states in weeks for every NBA player.
"""
def getNBAPlayerWeeklyStatsMatrix(nbaTeamWeeklyScheduleVectorDict, nbaPlayerStatsDict, items, session=None):

    nbaPlayerAvgStatsVectorDict = {}
    for nbaPlayerName in nbaPlayerStatsDict:
        # print nbaPlayerName
        nbaPlayerAvgStatsVector = []
        for item in items:
            if nbaPlayerStatsDict[nbaPlayerName]["GP"] == 0:
                nbaPlayerAvgStatsVector.append(0)
            else:
                nbaPlayerAvgStatsVector.append(float(nbaPlayerStatsDict[nbaPlayerName][item]) / float(nbaPlayerStatsDict[nbaPlayerName]["GP"]))
        # print nbaPlayerAvgStatsVector
        nbaPlayerAvgStatsVectorDict[nbaPlayerName] = nbaPlayerAvgStatsVector
    # print nbaPlayerAvgStatsVectorDict

    nbaPlayerWeeklyStatsMatrixDict = {}
    for nbaPlayerName in nbaPlayerStatsDict:
        # print nbaPlayerName
        teamAbbr = nbaPlayerStatsDict[nbaPlayerName]["TEAM_ABBREVIATION"]
        # print teamAbbr
        if teamAbbr == 0:
            teamWeeklyScheduleVector = [ 0 for (wdatefrom, wdateto) in WeekInfoList]
            nbaPlayerAvgStatsVector = [ 0 for item in items]
        else:
            teamWeeklyScheduleVector = nbaTeamWeeklyScheduleVectorDict[teamAbbr]
            nbaPlayerAvgStatsVector = nbaPlayerAvgStatsVectorDict[nbaPlayerName]
        # print teamWeeklyScheduleVector
        # print nbaPlayerAvgStatsVector
        teamWeeklyScheduleVector_tp = Matrix.Transpose(teamWeeklyScheduleVector)
        # print teamWeeklyScheduleVector_tp
        nbaPlayerWeeklyStatsMatrixDict[nbaPlayerName] = Matrix.Cross(teamWeeklyScheduleVector_tp, nbaPlayerAvgStatsVector)
        # print nbaPlayerWeeklyStatsMatrixDict[nbaPlayerName]
    # print nbaPlayerWeeklyStatsMatrixDict

    return nbaPlayerWeeklyStatsMatrixDict


"""
Generate a matrix for states in weeks for all fantasy teams.
"""
def getFantasyTeamWeeklyStatsMatrixDict(fantasyTeamList, nbaPlayerWeeklyStatsMatrixDict):

    fantasyTeamWeeklyStatsMatrixDict = {}
    for fantasyTeamInfo in fantasyTeamList:
        fantasyTeamName = fantasyTeamInfo["name"]
        # print fantasyTeamName
        fantasyTeamWeeklyStatsMatrix = None
        for nbaPlayerInfo in fantasyTeamInfo["roster"]:
            nbaPlayerName = nbaPlayerInfo["name"]
            # print nbaPlayerName
            # fantasyTeamWeeklyStatsMatrix
            # print nbaPlayerWeeklyStatsMatrixDict[nbaPlayerName]
            if fantasyTeamWeeklyStatsMatrix is None:
                fantasyTeamWeeklyStatsMatrix = nbaPlayerWeeklyStatsMatrixDict[nbaPlayerName]
            else:
                fantasyTeamWeeklyStatsMatrix = Matrix.Add(fantasyTeamWeeklyStatsMatrix, nbaPlayerWeeklyStatsMatrixDict[nbaPlayerName])
            # print fantasyTeamWeeklyStatsMatrix
        fantasyTeamWeeklyStatsMatrixDict[fantasyTeamName] = fantasyTeamWeeklyStatsMatrix
    # print fantasyTeamWeeklyStatsMatrixDict

    return fantasyTeamWeeklyStatsMatrixDict


"""
Generate a matrix for states in weeks merged opponent weekly stats by weekly opponents.
"""
def getFantasyTeamOpponentWeeklyStatsMatrix(fantasyTeamWeeklyStatsMatrixDict, myFantasyTeamInfo):

    myFantasyTeamName = myFantasyTeamInfo["name"]
    matchup = myFantasyTeamInfo["matchup"]
    # print matchup
    myFantasyTeamWeeklyStatsMatrix = fantasyTeamWeeklyStatsMatrixDict[myFantasyTeamName]
    dimension = len(myFantasyTeamWeeklyStatsMatrix[0])

    fantasyTeamOpponentWeeklyStatsMatrix = []
    for weekIdx, weeklyOpponent in enumerate(matchup):
        # print weekIdx, weeklyOpponent
        if weeklyOpponent not in fantasyTeamWeeklyStatsMatrixDict.keys():
            # print "no opponent stats found"
            opponentWeekStatsVector = [ float(0.0) for i in range(dimension)]
            # print opponentWeekStatsVector
        else:
            opponentWeeklyStatsMatrix = fantasyTeamWeeklyStatsMatrixDict[weeklyOpponent]
            # print opponentWeeklyStatsMatrix
            opponentWeekStatsVector = opponentWeeklyStatsMatrix[weekIdx]
            # print opponentWeekStatsVector
        fantasyTeamOpponentWeeklyStatsMatrix.append(opponentWeekStatsVector)
        # print fantasyTeamOpponentWeeklyStatsMatrix
    # print fantasyTeamOpponentWeeklyStatsMatrix

    return fantasyTeamOpponentWeeklyStatsMatrix


if __name__ == "__main__":
    year = "2017-18"
    myFantasyTeamName = "CHIYU"
    with requests.Session() as s:

        leagueInfo = fetchYahooFantasyLeagueInfo()
        # print leagueInfo
        usedNBAPlayerNameList = [playerInfo["name"] for fantasyTeamInfo in leagueInfo["teams"] for playerInfo in fantasyTeamInfo["roster"]]
        # print usedNBAPlayerNameList
        myFantasyTeamInfo = None
        for fantasyTeamInfo in leagueInfo["teams"]:
            if fantasyTeamInfo["name"] == myFantasyTeamName:
                myFantasyTeamInfo = fantasyTeamInfo
        # print myFantasyTeamInfo

        """ Generate a vector of games play in weeks for every NBA team. """
        yearSchedule = queryNBAYearSchedule(year, "full_schedule_%s.pickle" % (year), session=s, cache=True)
        # print json.dumps(yearSchedule, indent=4, sort_keys=True)
        allNBATeamSchedules = getAllTeamSchedules(yearSchedule)
        # print json.dumps(allNBATeamSchedules, indent=4, sort_keys=True)
        nbaTeamWeeklyScheduleVectorDict = getAllNBATeamScheduledWeeksVector(WeekInfoList, allNBATeamSchedules)
        # print nbaTeamWeeklyScheduleVectorDict

        nbaPlayerInfoDict = queryNBAPlayerInfoDict(year, session=s, cache=True)
        # print nbaPlayerInfoDict

        """ Try a list of different possible stats combination to see if any player is a strong candidates no matter in days or in weeks. """
        matchupItems = ["FG_PCT", "FT_PCT", "FG3M", "FG3_PCT"] + leagueInfo["items"][6:]
        overallImprovement = {}
        for statsHeader in matchupItems:
            overallImprovement[statsHeader] = 0

        candidatesDict = {}
        lastNGameList = [5]
        for n in lastNGameList:

            nbaPlayerRecentStatsDict = {}
            for nbaPlayerID, nbaPlayerInfo in nbaPlayerInfoDict.iteritems():
                nbaPlayerName = nbaPlayerInfo["PLAYER_NAME"]
                nbaPlayerRecentStatsDict[nbaPlayerName] = queryNBAPlayerRecentStatsInfo(nbaPlayerInfo, year, lastngames=n, session=s, cache=True)
            # print json.dumps(nbaPlayerRecentStatsDict, indent=4, sort_keys=True)
            nbaPlayerWeeklyStatsMatrixDict = getNBAPlayerWeeklyStatsMatrix(nbaTeamWeeklyScheduleVectorDict, nbaPlayerRecentStatsDict, leagueInfo["items"])
            # print nbaPlayerWeeklyStatsMatrixDict

            fantasyTeamWeeklyStatsMatrixDict = getFantasyTeamWeeklyStatsMatrixDict(leagueInfo["teams"], nbaPlayerWeeklyStatsMatrixDict)
            # print fantasyTeamWeeklyStatsMatrixDict
            fantasyTeamWeeklyStatsMatrix = fantasyTeamWeeklyStatsMatrixDict[myFantasyTeamName]
            # print fantasyTeamWeeklyStatsMatrix
            fantasyTeamOpponentWeeklyStatsMatrix = getFantasyTeamOpponentWeeklyStatsMatrix(fantasyTeamWeeklyStatsMatrixDict, myFantasyTeamInfo)
            # print fantasyTeamOpponentWeeklyStatsMatrix

            """ Start to examine the player one by one to see if any combination is better. """
            weekFrom = 5
            weekTo = 20

            """ Get the differences between my stats and the opponent's stats """
            fantasyTeamWeeklyMatchupStatsMatrix = statsMatrix2matchupMatrix(fantasyTeamWeeklyStatsMatrix)
            # print fantasyTeamWeeklyMatchupStatsMatrix
            fantasyTeamOpponentWeeklyMatchupStatsMatrix = statsMatrix2matchupMatrix(fantasyTeamOpponentWeeklyStatsMatrix)
            # print fantasyTeamOpponentWeeklyMatchupStatsMatrix
            fantasyTeamWeeklyMatchupResultMatrix = Matrix.Subtract(fantasyTeamWeeklyMatchupStatsMatrix, fantasyTeamOpponentWeeklyMatchupStatsMatrix)
            # print fantasyTeamWeeklyMatchupResultMatrix
            fantasyTeamWinnedWeeks = getMatchupResultWinnedWeeks(fantasyTeamWeeklyMatchupResultMatrix, weekFrom, weekTo)
            # print fantasyTeamWinnedWeeks

            """ Select Player One by One to See if any player is total placed by others. """
            for pickedNBAPlayerInfo in myFantasyTeamInfo["roster"]:
                pickedNBAPlayerName = pickedNBAPlayerInfo["name"]
                tmpFantasyTeamWeeklyStatsMatrix = copy.deepcopy(fantasyTeamWeeklyStatsMatrix)
                # print tmpFantasyTeamWeeklyStatsMatrix
                # print nbaPlayerWeeklyStatsMatrixDict[pickedNBAPlayerName]
                tmpFantasyTeamWeeklyStatsMatrix = Matrix.Subtract(tmpFantasyTeamWeeklyStatsMatrix, nbaPlayerWeeklyStatsMatrixDict[pickedNBAPlayerName])
                # print tmpFantasyTeamWeeklyStatsMatrix
                for cmpNBAPlayerName in nbaPlayerWeeklyStatsMatrixDict:
                    if cmpNBAPlayerName not in usedNBAPlayerNameList:
                        # print cmpNBAPlayerName
                        # print nbaPlayerWeeklyStatsMatrixDict[cmpNBAPlayerName]
                        newFantasyTeamWeeklyStatsMatrix = Matrix.Add(tmpFantasyTeamWeeklyStatsMatrix, nbaPlayerWeeklyStatsMatrixDict[cmpNBAPlayerName])
                        # print newFantasyTeamWeeklyStatsMatrix
                        newFantasyTeamWeeklyMatchupStatsMatrix = statsMatrix2matchupMatrix(newFantasyTeamWeeklyStatsMatrix)
                        # print newFantasyTeamWeeklyMatchupStatsMatrix
                        newFantasyTeamWeeklyMatchupResultMatrix = Matrix.Subtract(newFantasyTeamWeeklyMatchupStatsMatrix, fantasyTeamOpponentWeeklyMatchupStatsMatrix)
                        # print newFantasyTeamWeeklyMatchupResultMatrix
                        newFantasyTeamWinnedWeeks = getMatchupResultWinnedWeeks(newFantasyTeamWeeklyMatchupResultMatrix, weekFrom, weekTo)
                        # print newFantasyTeamWinnedWeeks
                        if newFantasyTeamWinnedWeeks > fantasyTeamWinnedWeeks:
                            if not candidatesDict.has_key(cmpNBAPlayerName):
                                candidatesDict[cmpNBAPlayerName] = []
                            candidatesDict[cmpNBAPlayerName].append({"player": cmpNBAPlayerName, "lastngames":n, "wins": newFantasyTeamWinnedWeeks, "replacement":pickedNBAPlayerName})
                            # print candidatesDict[cmpNBAPlayerName]

            # print json.dumps(candidatesDict, indent=4, sort_keys=True)

            newFantasyTeamWinnedWeeks = 0
            replacementCandidateDict = {}
            for candidatePlayerName in candidatesDict:
                for replacementInfo in candidatesDict[candidatePlayerName]:
                    replacementPlayerName = replacementInfo["replacement"]
                    wins = replacementInfo["wins"]
                    if newFantasyTeamWinnedWeeks < wins:
                        newFantasyTeamWinnedWeeks = wins
                    if not replacementInfo["replacement"] in replacementCandidateDict.keys():
                        replacementCandidateDict[replacementPlayerName] = {"candidates":{}, "maxWins": 0}
                    if replacementCandidateDict[replacementPlayerName]["maxWins"] < wins:
                        replacementCandidateDict[replacementPlayerName]["maxWins"] = wins
                    if not replacementCandidateDict[replacementPlayerName]["candidates"].has_key(wins):
                        replacementCandidateDict[replacementPlayerName]["candidates"][wins] = {}
                    if not replacementCandidateDict[replacementPlayerName]["candidates"][wins].has_key(candidatePlayerName):
                        replacementCandidateDict[replacementPlayerName]["candidates"][wins][candidatePlayerName] = []
                    replacementCandidateDict[replacementPlayerName]["candidates"][wins][candidatePlayerName].append(replacementInfo)
            # print json.dumps(replacementCandidateDict, indent=4, sort_keys=True)
            # print newFantasyTeamWinnedWeeks

            print "========== Player comparison bases on last %d games ==========" % (n)
            exemptPlayerNameList = ["Chandler Parsons", "Jeremy Lin"]
            for replacementName in replacementCandidateDict:
                maxWins = replacementCandidateDict[replacementName]["maxWins"]
                print "Replace %s with one of the following players to get %d wins:" % (replacementName, maxWins)
                itemValueChangeDict = {}
                for statsHeader in matchupItems:
                    itemValueChangeDict[statsHeader] = 0
                cmpPlayerCnt = 0
                for candidateName in replacementCandidateDict[replacementName]["candidates"][maxWins]:
                    if candidateName not in exemptPlayerNameList:
                        cmpPlayerCnt = cmpPlayerCnt + 1
                        replacementWeeklyMatchupStatsMatrix = statsMatrix2matchupMatrix(nbaPlayerWeeklyStatsMatrixDict[replacementName])
                        candidateWeeklyMatchupStatsMatrix = statsMatrix2matchupMatrix(nbaPlayerWeeklyStatsMatrixDict[candidateName])
                        diffWeeklyMatchupStatsMatrix = Matrix.Subtract(replacementWeeklyMatchupStatsMatrix, candidateWeeklyMatchupStatsMatrix)
                        # print diffWeeklyMatchupStatsMatrix
                        # print len(diffWeeklyMatchupStatsMatrix)
                        diffStatsVector = diffWeeklyMatchupStatsMatrix[0]
                        # print diffStatsVector
                        for i in range(1, len(diffWeeklyMatchupStatsMatrix)):
                            # print diffWeeklyMatchupStatsMatrix[i]
                            diffStatsVector = Matrix.Add(diffStatsVector, diffWeeklyMatchupStatsMatrix[i])
                        print ">> %s, stats: %s" % (candidateName, ",".join(["%s: %d" % (statsHeader, diffStatsVector[statsIdx]) for statsIdx, statsHeader in enumerate(matchupItems)]))
                        # print json.dumps(diffStatsVector, indent=4, sort_keys=True)
                        for statsIdx, statsValue in enumerate(diffStatsVector):
                            if statsValue > 0.0:
                                itemValueChangeDict[matchupItems[statsIdx]] = itemValueChangeDict[matchupItems[statsIdx]] + 1
                            elif statsValue < 0.0:
                                itemValueChangeDict[matchupItems[statsIdx]] = itemValueChangeDict[matchupItems[statsIdx]] - 1
                            else:
                                pass
                print ">> Overall stats changes: %s" % ",".join(["%s: %d" % (statsHeader, itemValueChangeDict[statsHeader]) for statsHeader in matchupItems])
                # print json.dumps(itemValueChangeDict, indent=4, sort_keys=True)

                for statsHeader in matchupItems:
                    if itemValueChangeDict[statsHeader] == cmpPlayerCnt:
                        overallImprovement[statsHeader] = overallImprovement[statsHeader] + 1
                    elif itemValueChangeDict[statsHeader] == (0 - cmpPlayerCnt):
                        overallImprovement[statsHeader] = overallImprovement[statsHeader] - 1
                    else:
                        pass

        print "========== Overall suggestion to improve your fantasy team =========="
        print "%s" % ",".join(["%s: %d" % (statsHeader, overallImprovement[statsHeader]) for statsHeader in matchupItems])
        # print json.dumps(overallImprovement, indent=4, sort_keys=True)

