from pydantic import BaseModel, Field
from typing import List, Optional, Dict



class AnalyzedMatch(BaseModel):
    # Same as a match ID except we attach the player's performance in the match with opponent laner's performance
    matchId: str
    date: int # unix timestamp? 
    playerId: str
    opponentId: str
    kills: int
    deaths: int
    assists: int
    dragons: int
    heralds: int
    barons: int
    win: bool
    score: float    
    opponentScore: float
    scoreDelta: float



class PerkStyleSelectionDto(BaseModel):
    perk: Optional[int] = None
    var1: Optional[int] = None
    var2: Optional[int] = None
    var3: Optional[int] = None

class PerkStyleDto(BaseModel):
    description: Optional[str] = None
    selections: Optional[List[PerkStyleSelectionDto]] = None
    style: Optional[int] = None

class PerkStatsDto(BaseModel):
    defense: Optional[int] = None
    flex: Optional[int] = None
    offense: Optional[int] = None

class PerksDto(BaseModel):
    statPerks: Optional[PerkStatsDto] = None
    styles: Optional[List[PerkStyleDto]] = None

class ParticipantDto(BaseModel):
    assists: Optional[int] = None
    baronKills: Optional[int] = None
    bountyLevel: Optional[int] = None
    champExperience: Optional[int] = None
    champLevel: Optional[int] = None
    championId: Optional[int] = None
    championName: Optional[str] = None
    championTransform: Optional[int] = None
    consumablesPurchased: Optional[int] = None
    damageDealtToBuildings: Optional[int] = None
    damageDealtToObjectives: Optional[int] = None
    damageDealtToTurrets: Optional[int] = None
    damageSelfMitigated: Optional[int] = None
    deaths: Optional[int] = None
    detectorWardsPlaced: Optional[int] = None
    doubleKills: Optional[int] = None
    dragonKills: Optional[int] = None
    firstBloodAssist: Optional[bool] = None
    firstBloodKill: Optional[bool] = None
    firstTowerAssist: Optional[bool] = None
    firstTowerKill: Optional[bool] = None
    gameEndedInEarlySurrender: Optional[bool] = None
    gameEndedInSurrender: Optional[bool] = None
    goldEarned: Optional[int] = None
    goldSpent: Optional[int] = None
    individualPosition: Optional[str] = None
    inhibitorKills: Optional[int] = None
    inhibitorTakedowns: Optional[int] = None
    inhibitorsLost: Optional[int] = None
    item0: Optional[int] = None
    item1: Optional[int] = None
    item2: Optional[int] = None
    item3: Optional[int] = None
    item4: Optional[int] = None
    item5: Optional[int] = None
    item6: Optional[int] = None
    itemsPurchased: Optional[int] = None
    killingSprees: Optional[int] = None
    kills: Optional[int] = None
    lane: Optional[str] = None
    largestCriticalStrike: Optional[int] = None
    largestKillingSpree: Optional[int] = None
    largestMultiKill: Optional[int] = None
    longestTimeSpentLiving: Optional[int] = None
    magicDamageDealt: Optional[int] = None
    magicDamageDealtToChampions: Optional[int] = None
    magicDamageTaken: Optional[int] = None
    neutralMinionsKilled: Optional[int] = None
    nexusKills: Optional[int] = None
    nexusTakedowns: Optional[int] = None
    nexusLost: Optional[int] = None
    objectivesStolen: Optional[int] = None
    objectivesStolenAssists: Optional[int] = None
    participantId: Optional[int] = None
    pentaKills: Optional[int] = None
    perks: Optional[PerksDto] = None
    physicalDamageDealt: Optional[int] = None
    physicalDamageDealtToChampions: Optional[int] = None
    physicalDamageTaken: Optional[int] = None
    profileIcon: Optional[int] = None
    puuid: Optional[str] = None
    quadraKills: Optional[int] = None
    riotIdName: Optional[str] = None
    riotIdTagline: Optional[str] = None
    role: Optional[str] = None
    sightWardsBoughtInGame: Optional[int] = None
    spell1Casts: Optional[int] = None
    spell2Casts: Optional[int] = None
    spell3Casts: Optional[int] = None
    spell4Casts: Optional[int] = None
    summoner1Casts: Optional[int] = None
    summoner1Id: Optional[int] = None
    summoner2Casts: Optional[int] = None
    summoner2Id: Optional[int] = None
    summonerId: Optional[str] = None
    summonerLevel: Optional[int] = None
    summonerName: Optional[str] = None
    teamEarlySurrendered: Optional[bool] = None
    teamId: Optional[int] = None
    teamPosition: Optional[str] = None
    timeCCingOthers: Optional[int] = None
    timePlayed: Optional[int] = None
    totalDamageDealt: Optional[int] = None
    totalDamageDealtToChampions: Optional[int] = None
    totalDamageShieldedOnTeammates: Optional[int]
    totalDamageTaken: Optional[int] = None
    totalHeal: Optional[int] = None
    totalHealsOnTeammates: Optional[int] = None
    totalMinionsKilled: Optional[int] = None
    totalTimeCCDealt: Optional[int] = None
    totalTimeSpentDead: Optional[int] = None
    totalUnitsHealed: Optional[int] = None
    tripleKills: Optional[int] = None
    trueDamageDealt: Optional[int] = None
    trueDamageDealtToChampions: Optional[int] = None
    trueDamageTaken: Optional[int] = None
    turretKills: Optional[int] = None
    turretTakedowns: Optional[int] = None
    turretsLost: Optional[int] = None
    unrealKills: Optional[int] = None
    visionScore: Optional[int] = None
    visionWardsBoughtInGame: Optional[int] = None
    wardsKilled: Optional[int] = None
    wardsPlaced: Optional[int] = None
    win: Optional[bool] = None

class ObjectiveDto(BaseModel): 
    first: bool
    kills: int

class ObjectivesDto(BaseModel):
    baron: ObjectiveDto
    champion: ObjectiveDto
    dragon: ObjectiveDto
    inhibitor: ObjectiveDto
    riftHerald: ObjectiveDto
    tower: ObjectiveDto


class TeamDto(BaseModel):
    teamId: Optional[int] = None
    win: Optional[bool] = None
    objectives: Optional[ObjectivesDto] = None

class InfoDto(BaseModel):
    gameCreation: Optional[float] = None # Unix in milliseconds
    gameDuration: Optional[float] = None
    gameEndTimestamp: Optional[float] = None
    gameId: Optional[float] = None
    gameMode: Optional[str] = None
    gameName: Optional[str] = None
    gameStartTimestamp: Optional[int] = None
    gameType: Optional[str] = None
    gameVersion: Optional[str] = None
    mapId: Optional[int] = None
    participants: Optional[List[ParticipantDto]] = None
    queueId: Optional[int] = None
    teams: Optional[List[TeamDto]] = None
    # Add more fields as necessary

class MetadataDto(BaseModel):
    dataVersion: Optional[str] = None
    matchId: Optional[str] = None
    participants: Optional[List[str]] = None

class Match(BaseModel):
    metadata: Optional[MetadataDto] = None
    info: Optional[InfoDto] = None
    puuid: Optional[str] = None
    processed: Optional[bool] = False

class AccountCreationRequest(BaseModel):
    gameName: str
    tagLine: str

class PatchStats(BaseModel):
    kills: Optional[int] = 0
    deaths: Optional[int] = 0
    assists: Optional[int] = 0
    games_played: Optional[int] = 0
    kda_ratio: Optional[float] = 0.0
    wins: Optional[int] = 0
    losses: Optional[int] = 0
    win_rate: Optional[float] = 0.0
    score: Optional[List[float]] = 0.0
    average_score: Optional[float] = 0.0
    score_std: Optional[float] = 0.0
    opponent_delta: Optional[List[float]] = 0.0
    average_delta: Optional[float] = 0.0
    opponent_delta_std: Optional[float] = 0.0

class Account(BaseModel):
    puuid: str  # Riot's unique identifier for a player
    gameName: str
    tagLine: str
    lastUpdated: int = 0 # Unix timestamp, 0 by default
    matchHistory: Optional[List[str]] = None  # List of match IDs
    # matches: Optional[List[Match]]
    analyzed_matchHistory: Optional[List[AnalyzedMatch]] = None  # List of match IDs that have been analyzed
    playerId: Optional[str]
    stats_by_patch: Dict[str, PatchStats] = Field(default_factory=dict)  # Stats organized by patch