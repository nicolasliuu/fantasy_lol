from pydantic import BaseModel
from typing import List, Optional

class Account(BaseModel):
    puuid: Optional[str] = None  # Riot's unique identifier for a player
    gameName: Optional[str] = None
    tagLine: Optional[str] = None
    matchHistory: Optional[List[str]] = None  # List of match IDs
    playerId: Optional[str] = None  # Your custom player ID

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