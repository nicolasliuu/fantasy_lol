from pydantic import BaseModel
from typing import List, Optional
from typing import List, Optional
from .models import AnalyzedMatch

class Account(BaseModel):
    puuid: str  # Riot's unique identifier for a player
    gameName: str
    tagLine: str
    matchHistory: Optional[List[str]] = None  # List of match IDs
    analyzed_matchHistory: Optional[List[AnalyzedMatch]] = None  # List of match IDs that have been analyzed
    playerId: Optional[str] = None  # Your custom player ID
    kills: Optional[List[int]] # Number of kills for current period (patch)
    deaths: Optional[List[int]] # Number of deaths for current period (patch)
    assists: Optional[List[int]] # Number of assists for current period (patch)
    kda_ratio: Optional[List[float]] # KDA ratio for current period (patch)
    wins: Optional[List[int]] # Number of wins for current period (patch)
    losses: Optional[List[int]] # Number of losses for current period (patch)
    win_rate: Optional[List[float]] # Win rate for current period (patch)
    score: Optional[List[float]] # AI-computed Score for current period (patch)
    score_std: Optional[List[float]] # Standard deviation of AI-computed Score for current period (patch)
    opponent_delta: Optional[List[float]] # Difference in AI-computed Score between player and opponent for current period (patch)

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
    puuid: Optional[str] = None
    summonerName: Optional[str] = None
    championName: Optional[str] = None
    kills: Optional[int] = None
    deaths: Optional[int] = None
    assists: Optional[int] = None
    win: Optional[bool] = None
    perks: Optional[PerksDto] = None
    
    # Add more fields as necessary

class TeamDto(BaseModel):
    teamId: Optional[int] = None
    win: Optional[bool] = None
    # Consider adding a detailed schema for bans and objectives if needed

class InfoDto(BaseModel):
    gameCreation: Optional[float] = None
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

class AccountCreationRequest(BaseModel):
    gameName: str
    tagLine: str