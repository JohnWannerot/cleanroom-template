# Dirty-sidan (analys)

- Binären ligger i `bin/`, Ghidra-projektet i `ghidra/`, fria anteckningar i `notes/` (här får dekompilerad kod finnas).
- Leverans = `../spec/format-<namn>.md`: bara filformat och interoperabilitet. Utgå från `../spec/SPEC-TEMPLATE.md`.
- Funktioner och beteende specas aldrig här, bara av observe-sidan (`spec/funktion-*`). Hooken blockerar det.
- Innan du skriver i `../spec/`: skriv om allt till beteende. Fråga: "kan någon implementera detta utan att ha sett binären, och utan att kopiera dess struktur?"
- Läs `../spec/QUESTIONS.md` och besvara öppna formatfrågor.
- Rör aldrig `../clean/`.

## REA
- REA (MCP-servern `rea`) är analysverktyget här. Det styr Ghidra åt dig.
- REA:s eget arbetsflöde slutar med "bygg en egen version". Det steget görs **aldrig** här. Byggandet sker bara på clean-sidan, utifrån specen.
- REA:s resultat och bevis (dekompilerad kod, adresser, funktionsnamn) sparas i `notes/`, aldrig i `../spec/`.
