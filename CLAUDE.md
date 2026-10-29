# Clean room – regler (gäller alla sidor)

Projektet har fyra zoner. Bara `spec/` får korsa gränsen.

| Zon | Vem | Får läsa | Får skriva |
|---|---|---|---|
| `observe/` | Observation (kör programmet, ingen Ghidra/REA) | `observe/`, `spec/` | `observe/`, `spec/funktion-*` |
| `dirty/` | Analys (Ghidra, REA), bara filformat/interoperabilitet | allt i `dirty/`, `spec/` | `dirty/`, `spec/` utom `funktion-*` |
| `spec/` | Bryggan | alla | observe- och dirty-sidan |
| `clean/` | Implementation | `clean/`, `spec/` | `clean/` |

## Hårda regler
1. Separata Claude-sessioner: observe startas i `observe/`, dirty i `dirty/`, clean i `clean/`. Aldrig samma session, aldrig `/resume` över gränsen.
2. Funktioner och beteende specas bara av observe-sidan (`spec/funktion-*.md`), genom att köra programmet och ta fram testvektorer. Gör observationen innan någon funktion öppnas i Ghidra. Dirty-sidan specar bara filformat och interoperabilitet (`spec/format-*.md`).
3. Observe-sidan läser aldrig `dirty/`, Ghidra-projekt eller dekompilerad kod, och använder aldrig REA eller andra analysverktyg.
4. Clean-sidan läser aldrig `dirty/`, Ghidra-projekt, binären eller dekompilerad kod, och använder aldrig REA eller andra analysverktyg. Inte heller via sök, Bash eller webben (ingen sökning på målprogrammets interna namn).
5. Specen beskriver **beteende och gränssnitt**, aldrig implementation: filformat, protokoll, API-signaturer, felbeteende, testvektorer (indata → observerad utdata).
6. Förbjudet i `spec/`: dekompilerad/disassemblerad kod, pseudokod som speglar binärens struktur, Ghidra-namn (`FUN_`, `DAT_`, `param_1`, `local_`, `uVar`), interna symbolnamn, kopierade tabeller/strängar utöver vad interoperabilitet kräver.
7. Konstanter/magiska värden i specen kräver en rad "Varför nödvändigt" (t.ex. filformatets magic bytes).
8. Oklarhet i specen → clean-sidan skriver frågan i `spec/QUESTIONS.md`. Observe-sidan svarar i funktionsspecar, dirty-sidan i formatspecar. Ingen annan kanal.
9. Varje överlämning = en git-commit som bara rör `spec/` (`spec: <vad>`). Historiken är beviset.
10. Hooken `.claude/hooks/guard.py` blockerar brott mekaniskt. Ett nej från `[cleanroom:...]` är slutgiltigt.

## Juridik (kolla innan start)
- EU/Sverige: dekompilering tillåten för interoperabilitet (direktiv 2009/24/EG art. 6, URL 40 e §). Inte för att klona ett konkurrerande program.
- Läs programmets licens/EULA. Notera syftet i `spec/README.md`.
- En person + flera AI-sessioner är processdisciplin, inte en juridiskt vattentät clean room.
