# G3: recommended validation protocol

R1 SUPPORTED; R2 NOT_SUPPORTED; R3 SUPPORTED.

|Group|RP complete/planned|Ordinary median (%)|RP median (%)|Worst RP (%)|RP >10%|F fallback / planned|
|---|---:|---:|---:|---:|---:|---:|
|weekly|60/60|14.627468|0.000000|80.983970|8|32/60|
|cftc|34/34|14.627468|0.000000|80.983970|7|12/34|
|nyfed|26/26|15.051464|0.000000|25.508964|1|20/26|
|fx|2/2|-15.695164|-15.695164|-14.766763|0|0/2|

|FX period|Ordinary (%)|RP (%)|Half-gain threshold (%)|Route|R3|
|---|---:|---:|---:|---|---|
|original|-14.766763|-14.766763|-7.383381|QR|SUPPORTED|
|early2015|-16.623565|-16.623565|-8.311783|QR|SUPPORTED|

Retrospective heuristic designed after prior results. Equal-cell normalized losses, no independent-series combined test or prospective protection guarantee; unavailable fits are never credited as successful fallback.

Rows, all candidates, sealed validation selections/gates and references retain all failures. No failure is credited as a successful return toF.
