# Clean room – regler (gäller båda sidor)

Projektet har tre zoner. Bara `spec/` får korsa gränsen.

| Zon | Vem | Får läsa | Får skriva |
|---|---|---|---|
| `dirty/` | Analys (Ghidra, REA) | allt i `dirty/`, `spec/` | `dirty/`, `spec/` |
| `spec/` | Bryggan | båda | bara dirty-sidan |
| `clean/` | Implementation | `clean/`, `spec/` | `clean/` |

## Hårda regler
1. Två separata Claude-sessioner: dirty startas i `dirty/`, clean i `clean/`. Aldrig samma session, aldrig `/resume` över gränsen.
2. Clean-sidan läser aldrig `dirty/`, Ghidra-projekt, binären eller dekompilerad kod, och använder aldrig REA eller andra analysverktyg. Inte heller via sök, Bash eller webben (ingen sökning på målprogrammets interna namn).
3. Specen beskriver **beteende och gränssnitt**, aldrig implementation: filformat, protokoll, API-signaturer, felbeteende, testvektorer (indata → observerad utdata).
4. Förbjudet i `spec/`: dekompilerad/disassemblerad kod, pseudokod som speglar binärens struktur, Ghidra-namn (`FUN_`, `DAT_`, `param_1`, `local_`, `uVar`), interna symbolnamn, kopierade tabeller/strängar utöver vad interoperabilitet kräver.
5. Konstanter/magiska värden i specen kräver en rad "Varför nödvändigt" (t.ex. filformatets magic bytes).
6. Oklarhet i specen → clean-sidan skriver frågan i `spec/QUESTIONS.md`. Dirty-sidan svarar i specen. Ingen annan kanal.
7. Varje överlämning = en git-commit som bara rör `spec/` (`spec: <vad>`). Historiken är beviset.
8. Hooken `.claude/hooks/guard.py` blockerar brott mekaniskt. Ett nej från `[cleanroom:...]` är slutgiltigt.

## Juridik (kolla innan start)
- EU/Sverige: dekompilering tillåten för interoperabilitet (direktiv 2009/24/EG art. 6, URL 40 e §). Inte för att klona ett konkurrerande program.
- Läs programmets licens/EULA. Notera syftet i `spec/README.md`.
- En person + två AI-sessioner är processdisciplin, inte en juridiskt vattentät clean room.
