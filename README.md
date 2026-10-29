# cleanroom-template

Mall för **clean room reverse engineering** med Ghidra (valfritt via [REA](https://github.com/morluto/rea)) och två separata Claude Code-sessioner.

En session analyserar programmet (dirty). En annan bygger en ny implementation (clean) och ser bara en skriftlig spec. En hook stoppar läckor mekaniskt.

## Struktur

```
dirty/          Analys: binären (bin/), Ghidra-projekt (ghidra/), anteckningar (notes/)
spec/           Enda bryggan: SPEC-TEMPLATE.md, QUESTIONS.md, README.md
clean/          Ny implementation, skriven bara utifrån spec/
.claude/hooks/  guard.py: blockerar regelbrott
CLAUDE.md       Reglerna, som båda sessionerna läser
```

| Zon | Får läsa | Får skriva |
|---|---|---|
| `dirty/` | `dirty/`, `spec/` | `dirty/`, `spec/` |
| `clean/` | `clean/`, `spec/` | `clean/` |

## Kom igång

Krav: [Claude Code](https://claude.com/claude-code), Python 3, git, [Ghidra](https://github.com/NationalSecurityAgency/ghidra) (JDK 21). Valfritt: REA (Node.js), se nedan.

```powershell
$n='mittprojekt'; git clone https://github.com/JohnWannerot/cleanroom-template "$n"; cd "$n"; Remove-Item -Recurse -Force .git; git init; git add -A; git commit -m "init clean room"
```

1. Lägg binären i `dirty/bin/` och fyll i `spec/README.md` (syfte och licens).
2. Analys: `cd dirty; claude`. Skriv en spec per komponent utifrån `spec/SPEC-TEMPLATE.md`.
3. Committa specen: `git add spec; git commit -m "spec: <vad>"`.
4. Implementation: starta en **ny** session med `cd clean; claude`.
5. Frågor från clean-sidan skrivs i `spec/QUESTIONS.md`. Dirty-sidan svarar i specen.

## REA (valfritt)

[REA](https://github.com/morluto/rea) är en MCP-server som låter Claude styra Ghidra. Installera den bara för dirty-sidan. Kör **inte** `npx rea-agents setup` för Claude Code, eftersom det registrerar REA i alla projekt, även på clean-sidan.

```powershell
npm install --global rea-agents; cd dirty; claude mcp add --scope local rea -- node "$(npm root -g)\rea-agents\scripts\rea.mjs" mcp
```

`--scope local` gör att REA bara laddas när Claude startas i `dirty/`. Hooken blockerar ändå REA på clean-sidan.

## Vad hooken stoppar

| Försök | Resultat |
|---|---|
| Clean-sessionen läser något i `dirty/` eller Ghidra-filer | Blockeras |
| Dirty-sessionen skriver Ghidra-artefakter (`FUN_`, `DAT_`, `param_1`, `local_`, `uVar3` …) i `spec/` | Blockeras |
| Clean-sessionen anropar REA (MCP-verktyg eller `rea`-kommandot) | Blockeras |
| Någon av sessionerna ändrar hooken eller dess inställningar | Blockeras |

Hooken matchar text i sökvägar och fungerar inte som en sandlåda. Starta därför alltid varje session i sin egen mapp.

## Exempel

Ett nedlagt musikprogram sparar låtar som `.bbx`. Du vill att din app ska kunna öppna dem.

- **Dirty** ser i Ghidra `if (param_1[0] == 0x42 && param_1[1] == 0x42)`.
- **Spec** säger: "Filen börjar med `BB`, följt av antal spår. Varje spår har ett namn på max 32 tecken och en volym 0–100." Specen har också testvektorer.
- **Clean** skriver tester från testvektorerna och sedan en egen parser, utan att ha sett originalkoden.

## Juridik

- EU/Sverige: dekompilering är tillåten för interoperabilitet (direktiv 2009/24/EG art. 6, URL 40 e §). Den är inte tillåten för att klona ett konkurrerande program.
- Läs målprogrammets licens innan du börjar.
- En person med två AI-sessioner följer en disciplinerad process. Det är inte en juridiskt vattentät clean room. Detta är ingen juridisk rådgivning.

## Licens

[MIT-0](LICENSE): använd fritt, inget krav på att ta med licenstexten i dina projekt.
