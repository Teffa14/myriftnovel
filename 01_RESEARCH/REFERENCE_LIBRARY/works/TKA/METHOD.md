# Método
Python: ZIP, BeautifulSoup html.parser. Archivos EPUB/chap_{i:02d}.xhtml; validar 1–1729, extraer número del h1. Texto de p no vacíos con get_text(' ',strip=True). Excluir notas por prefijos T/N:, TL/N:, Translator's Note:, Editor's Note:, Announcement:, Also, please check out the Author (variantes). Excluir 1729 del corpus. Palabras regex [A-Za-z0-9]+(?:[’'\\-][A-Za-z0-9]+)*. Comillas dobles emparejadas por párrafo, inicios con comillas, puntuación literal; oraciones aproximadas por grupos de .!? seguidos de cierres opcionales y espacio/fin (mínimo uno por párrafo). Lexicones insensibles a mayúsculas con límites de palabra:
competition match(es), tournament, playoff(s), championship, round(s), arena, opponent(s);
institutions club, guild, alliance, manager, sponsor, contract, captain, team;
mechanics skill(s), damage, health, cooldown, equipment, combo, attack, defense, mana, dungeon;
spectators spectator(s), audience, viewer(s), fan(s), commentator(s), broadcast;
economic money, price, cost, salary, contract, sponsor, budget, pay, paid, profit, financial, rent;
uncertainty perhaps, maybe, probably, possible, likely, guess, suspect, uncertain, wonder;
cognition thought, think, thinking, realized, understood, noticed, knew, know, expected, plan, strategy.
CSV verificado: 1728 filas, suma words 3154011. Ambos identificadores preservados. No almacenar textos originales. Métricas de traducción, no firma autoral china.
