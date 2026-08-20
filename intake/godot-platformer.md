# Godot 2D Platformer — "JumpQuest"

## Vision
Ein charmantes 2D-Platformer-Spiel in Godot 4, in dem der Spieler durch Level springt,
Münzen sammelt und Hindernissen ausweicht. Ziel: 10 Level, lokale Highscores, veröffentlicht
auf itch.io.

## Problem / Motivation
Der Markt für kleine, charmante Indie-Platformer wächst. Ein kleines, fokussiertes Spiel
mit sauberem Game-Feel ist schneller veröffentlicht als ein großes Projekt.

## Zielgruppe
- Casual Gamer (18-35), die kurze Spielsessions mögen
- Indie-Game-Community (itch.io)

## Scope (In Scope)
- Godot 4 Projektstruktur
- Player-Charakter mit Bewegung (Double Jump, Coyote Time, Jump Buffer)
- 3 Beispiel-Level mit Tilemap, Kollisionen, Gegnern
- Münzen + Highscore-System (lokal, JSON)
- Pause-Menü, Game Over Screen, HUD
- Export-Preset für itch.io (HTML5 + Windows)

## Nicht im Scope
- Multiplayer
- Online-Scores
- Story/Kampagne
- Sound-Design-Outsourcing

## Technische Hinweise
- Engine: Godot 4.7 (GDScript)
- Tilemap mit Auto-Tiling
- CharacterBody2D für den Player
- Level-Daten als .tscn-Szenen

## Monetarisierung
- Free auf itch.io, Spenden-Payment optional (Pay-What-You-Want)
- Kein Abo, keine In-App-Käufe
