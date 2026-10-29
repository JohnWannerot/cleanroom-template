# cleanroom-template

Mall för **clean room reverse engineering** med Ghidra (valfritt via [REA](https://github.com/morluto/rea)) och två separata Claude Code-sessioner.

En session observerar programmet när det körs och specar funktionerna (observe). En annan analyserar binären i Ghidra, men bara för filformat (dirty). En tredje bygger en ny implementation (clean) och ser bara en skriftlig spec. En hook stoppar läckor mekaniskt.

## Struktur

```
observe/        Observation: kör programmet, anteckningar (notes/), ingen Ghidra
dirty/          Analys: binären (bin/), Ghidra-projekt (ghidra/), anteckningar (notes/)
spec/           Enda bryggan: SPEC-TEMPLATE.md, QUESTIONS.md, README.md
clean/          Ny implementation, skriven bara utifrån spec/
.claude/hooks/  guard.py: blockerar regelbrott
CLAUDE.md       Reglerna, som båda sessionerna läser
```

| Zon | Får läsa | Får skriva |
|---|---|---|
| `observe/` | `observe/`, `spec/` | `observe/`, `spec/funktion-*` |
| `dirty/` | `dirty/`, `spec/` | `dirty/`, `spec/format-*` |
| `clean/` | `clean/`, `spec/` | `clean/` |

## Kom igång

Krav: [Claude Code](https://claude.com/claude-code), Python 3, git, [Ghidra](https://github.com/NationalSecurityAgency/ghidra) (JDK 21). Valfritt: REA (Node.js), se nedan.

```powershell
$n='mittprojekt'; git clone https://github.com/JohnWannerot/cleanroom-template "$n"; cd "$n"; Remove-Item -Recurse -Force .git; git init; git add -A; git commit -m "init clean room"
```

1. Lägg binären i `dirty/bin/` och fyll i `spec/README.md` (syfte och licens).
2. Observation **först**: `cd observe; claude`. Kör programmet (helst i en VM utan nätverk) och skriv `spec/funktion-<namn>.md` utifrån `spec/SPEC-TEMPLATE.md`.
3. Analys, bara filformat: `cd dirty; claude`. Skriv `spec/format-<namn>.md`.
4. Committa specen: `git add spec; git commit -m "spec: <vad>"`.
5. Implementation: starta en **ny** session med `cd clean; claude`.
6. Frågor från clean-sidan skrivs i `spec/QUESTIONS.md`. Observe-sidan svarar om funktioner, dirty-sidan om format.

## REA (valfritt)

[REA](https://github.com/morluto/rea) är en MCP-server som låter Claude styra Ghidra. Installera den bara för dirty-sidan. Kör **inte** `npx rea-agents setup` för Claude Code, eftersom det registrerar REA i alla projekt, även på clean-sidan.

```powershell
npm install --global rea-agents; cd dirty; claude mcp add --scope local rea -- node "$(npm root -g)\rea-agents\scripts\rea.mjs" mcp
```

`--scope local` gör att REA bara laddas när Claude startas i `dirty/`. Hooken blockerar ändå REA på clean-sidan.

## Vad hooken stoppar

| Försök | Resultat |
|---|---|
| Clean- eller observe-sessionen läser något i `dirty/` eller Ghidra-filer | Blockeras |
| Dirty-sessionen skriver en funktionsspec (`spec/funktion-*`) | Blockeras |
| Dirty-sessionen skriver Ghidra-artefakter (`FUN_`, `DAT_`, `param_1`, `local_`, `uVar3` …) i `spec/` | Blockeras |
| Clean- eller observe-sessionen anropar REA (MCP-verktyg eller `rea`-kommandot) | Blockeras |
| Någon av sessionerna ändrar hooken eller dess inställningar | Blockeras |

Hooken matchar text i sökvägar och fungerar inte som en sandlåda. Starta därför alltid varje session i sin egen mapp.

## Exempel

Ett nedlagt musikprogram sparar låtar som `.bbx`. Du vill att din app ska kunna öppna dem.

- **Dirty** ser i Ghidra `if (param_1[0] == 0x42 && param_1[1] == 0x42)`.
- **Spec** säger: "Filen börjar med `BB`, följt av antal spår. Varje spår har ett namn på max 32 tecken och en volym 0–100." Specen har också testvektorer.
- **Clean** skriver tester från testvektorerna och sedan en egen parser, utan att ha sett originalkoden.

## Juridik

- EU/Sverige: dekompilering är tillåten för interoperabilitet (direktiv 2009/24/EG art. 6, URL 40 e §). Den är inte tillåten för att klona ett konkurrerande program.
- Att köra och observera programmet är alltid tillåtet för den som får använda det (art. 5.3), och funktionalitet är inte skyddad (EU-domstolen, *SAS Institute*, C-406/10). Därför specas funktioner av observe-sidan och aldrig från dekompilerad kod.
- Läs målprogrammets licens innan du börjar.
- En person med flera AI-sessioner följer en disciplinerad process. Det är inte en juridiskt vattentät clean room. Detta är ingen juridisk rådgivning.

## Licens

[MIT-0](LICENSE): använd fritt, inget krav på att ta med licenstexten i dina projekt.
