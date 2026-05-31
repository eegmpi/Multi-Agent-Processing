<div align="center">

<img src="https://pbs.twimg.com/profile_images/2061190710175432705/_HOK3T47_400x400.jpg" alt="EEG-MPI Logo" width="160" style="border-radius: 50%;"/>

# EEG-MPI
### Multi-Agent Processing Interface for EEG Brain Signals

[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.4.1-cyan?style=flat-square)](CHANGELOG.md)
[![Build](https://img.shields.io/github/actions/workflow/status/eeg-mpi/eeg-mpi/ci.yml?style=flat-square&label=CI)](/.github/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/Coverage-94%25-brightgreen?style=flat-square)]()
[![Stars](https://img.shields.io/github/stars/eeg-mpi/eeg-mpi?style=flat-square&color=yellow)](https://github.com/eeg-mpi/eeg-mpi/stargazers)
[![Twitter](https://img.shields.io/badge/Follow-@eeg__mpi-black?style=flat-square&logo=x)](https://x.com/eeg_mpi)

**A next-generation neurotechnology platform where 5 specialized AI agents collaborate  
in real-time to process, analyze, and interpret EEG brain signals.**

[🚀 Quick Start](#-quick-start) · [📖 Docs](docs/) · [🤖 Agents](#-agent-pipeline) · [💬 Community](https://x.com/eeg_mpi)

</div>

---

<div align="center">
<img src="data:image/svg+xml;base64,PHN2ZyB2aWV3Qm94PSIwIDAgMTIwMCAyMjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgc3R5bGU9ImJhY2tncm91bmQ6IzA0MDYwQzsiPgogIDxkZWZzPgogICAgPHN0eWxlPgogICAgICBAa2V5ZnJhbWVzIHdhdmUgewogICAgICAgIDAlICAgeyBzdHJva2UtZGFzaG9mZnNldDogMDsgfQogICAgICAgIDEwMCUgeyBzdHJva2UtZGFzaG9mZnNldDogLTQwMDsgfQogICAgICB9CiAgICAgIEBrZXlmcmFtZXMgcHVsc2UgewogICAgICAgIDAlLCAxMDAlIHsgb3BhY2l0eTogMC42OyB9CiAgICAgICAgNTAlICAgICAgIHsgb3BhY2l0eTogMTsgfQogICAgICB9CiAgICAgIEBrZXlmcmFtZXMgZGFzaC1mbG93IHsKICAgICAgICAwJSAgIHsgc3Ryb2tlLWRhc2hvZmZzZXQ6IDIwOyB9CiAgICAgICAgMTAwJSB7IHN0cm9rZS1kYXNob2Zmc2V0OiAwOyB9CiAgICAgIH0KICAgICAgLmVlZy13YXZlIHsKICAgICAgICBzdHJva2U6ICMwMEZGRUE7CiAgICAgICAgc3Ryb2tlLXdpZHRoOiAyOwogICAgICAgIGZpbGw6IG5vbmU7CiAgICAgICAgc3Ryb2tlLWRhc2hhcnJheTogOCA0OwogICAgICAgIGFuaW1hdGlvbjogd2F2ZSAzcyBsaW5lYXIgaW5maW5pdGU7CiAgICAgICAgZmlsdGVyOiBkcm9wLXNoYWRvdygwIDAgNHB4ICMwMEZGRUEpOwogICAgICB9CiAgICAgIC5lZWctd2F2ZS0yIHsKICAgICAgICBzdHJva2U6ICNBODU1Rjc7CiAgICAgICAgc3Ryb2tlLXdpZHRoOiAxLjU7CiAgICAgICAgZmlsbDogbm9uZTsKICAgICAgICBzdHJva2UtZGFzaGFycmF5OiA2IDM7CiAgICAgICAgYW5pbWF0aW9uOiB3YXZlIDRzIGxpbmVhciBpbmZpbml0ZTsKICAgICAgICBvcGFjaXR5OiAwLjU7CiAgICAgIH0KICAgICAgLm5vZGUtYm94IHsKICAgICAgICByeDogODsKICAgICAgICBmaWxsOiAjMEQxMTE3OwogICAgICAgIHN0cm9rZS13aWR0aDogMS41OwogICAgICB9CiAgICAgIC5ub2RlLWxhYmVsIHsKICAgICAgICBmb250LWZhbWlseTogJ0NvdXJpZXIgTmV3JywgQ291cmllciwgbW9ub3NwYWNlOwogICAgICAgIGZvbnQtc2l6ZTogOXB4OwogICAgICAgIGZpbGw6ICNDQkQ1RTE7CiAgICAgICAgdGV4dC1hbmNob3I6IG1pZGRsZTsKICAgICAgfQogICAgICAubm9kZS1pZCB7CiAgICAgICAgZm9udC1mYW1pbHk6ICdDb3VyaWVyIE5ldycsIENvdXJpZXIsIG1vbm9zcGFjZTsKICAgICAgICBmb250LXNpemU6IDhweDsKICAgICAgICB0ZXh0LWFuY2hvcjogbWlkZGxlOwogICAgICB9CiAgICAgIC5jb25uZWN0b3IgewogICAgICAgIHN0cm9rZS13aWR0aDogMTsKICAgICAgICBzdHJva2UtZGFzaGFycmF5OiA0IDM7CiAgICAgICAgZmlsbDogbm9uZTsKICAgICAgICBhbmltYXRpb246IGRhc2gtZmxvdyAxcyBsaW5lYXIgaW5maW5pdGU7CiAgICAgIH0KICAgICAgLnRpdGxlLXRleHQgewogICAgICAgIGZvbnQtZmFtaWx5OiAnQ291cmllciBOZXcnLCBDb3VyaWVyLCBtb25vc3BhY2U7CiAgICAgICAgZm9udC13ZWlnaHQ6IGJvbGQ7CiAgICAgICAgZmlsbDogIzAwRkZFQTsKICAgICAgICBmaWx0ZXI6IGRyb3Atc2hhZG93KDAgMCA2cHggIzAwRkZFQSk7CiAgICAgIH0KICAgICAgLnN1YnRpdGxlLXRleHQgewogICAgICAgIGZvbnQtZmFtaWx5OiAnQ291cmllciBOZXcnLCBDb3VyaWVyLCBtb25vc3BhY2U7CiAgICAgICAgZmlsbDogI0E4NTVGNzsKICAgICAgfQogICAgICAubm9kZS1wdWxzZSB7CiAgICAgICAgYW5pbWF0aW9uOiBwdWxzZSAycyBlYXNlLWluLW91dCBpbmZpbml0ZTsKICAgICAgfQogICAgPC9zdHlsZT4KCiAgICA8IS0tIEdsb3cgZmlsdGVyIC0tPgogICAgPGZpbHRlciBpZD0iZ2xvdy1jeWFuIj4KICAgICAgPGZlR2F1c3NpYW5CbHVyIHN0ZERldmlhdGlvbj0iMiIgcmVzdWx0PSJibHVyIi8+CiAgICAgIDxmZU1lcmdlPjxmZU1lcmdlTm9kZSBpbj0iYmx1ciIvPjxmZU1lcmdlTm9kZSBpbj0iU291cmNlR3JhcGhpYyIvPjwvZmVNZXJnZT4KICAgIDwvZmlsdGVyPgogICAgPGZpbHRlciBpZD0iZ2xvdy12aW9sZXQiPgogICAgICA8ZmVHYXVzc2lhbkJsdXIgc3RkRGV2aWF0aW9uPSIyIiByZXN1bHQ9ImJsdXIiLz4KICAgICAgPGZlTWVyZ2U+PGZlTWVyZ2VOb2RlIGluPSJibHVyIi8+PGZlTWVyZ2VOb2RlIGluPSJTb3VyY2VHcmFwaGljIi8+PC9mZU1lcmdlPgogICAgPC9maWx0ZXI+CiAgPC9kZWZzPgoKICA8IS0tIEJhY2tncm91bmQgZ3JpZCAtLT4KICA8cGF0dGVybiBpZD0iZ3JpZCIgd2lkdGg9IjQwIiBoZWlnaHQ9IjQwIiBwYXR0ZXJuVW5pdHM9InVzZXJTcGFjZU9uVXNlIj4KICAgIDxwYXRoIGQ9Ik0gNDAgMCBMIDAgMCAwIDQwIiBmaWxsPSJub25lIiBzdHJva2U9IiMwRDFCMkEiIHN0cm9rZS13aWR0aD0iMC41Ii8+CiAgPC9wYXR0ZXJuPgogIDxyZWN0IHdpZHRoPSIxMjAwIiBoZWlnaHQ9IjIyMCIgZmlsbD0idXJsKCNncmlkKSIvPgoKICA8IS0tIFRpdGxlIC0tPgogIDx0ZXh0IHg9IjYwMCIgeT0iMzAiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGNsYXNzPSJ0aXRsZS10ZXh0IiBmb250LXNpemU9IjIyIj5FRUctTVBJPC90ZXh0PgogIDx0ZXh0IHg9IjYwMCIgeT0iNDgiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGNsYXNzPSJzdWJ0aXRsZS10ZXh0IiBmb250LXNpemU9IjEwIj5NdWx0aS1BZ2VudCBQcm9jZXNzaW5nIEludGVyZmFjZSDCtyBSZWFsLXRpbWUgRUVHIEJyYWluIFNpZ25hbCBQaXBlbGluZTwvdGV4dD4KCiAgPCEtLSBFRUcgV2F2ZSAodG9wKSAtLT4KICA8cG9seWxpbmUgY2xhc3M9ImVlZy13YXZlIiBwb2ludHM9IgogICAgMCw4MCAyMCw4MCAzMCw2MCA0MCwxMDAgNTAsNzUgNjAsODAgNzAsNTUgODUsMTA1IDEwMCw2NSAxMTUsODAKICAgIDEzMCw4MCAxNDUsNTggMTYwLDEwMiAxNzUsNzIgMTkwLDgwIDIwNSw1MyAyMjAsMTA4IDIzNSw2MiAyNTAsODAKICAgIDI2NSw4MCAyODAsNjAgMjk1LDEwMCAzMTAsNzUgMzI1LDgwIDM0MCw1NSAzNTUsMTA1IDM3MCw2NSAzODUsODAKICAgIDQwMCw4MCA0MTUsNTggNDMwLDEwMiA0NDUsNzIgNDYwLDgwIDQ3NSw1MyA0OTAsMTA4IDUwNSw2MiA1MjAsODAKICAgIDUzNSw4MCA1NTAsNjAgNTY1LDEwMCA1ODAsNzUgNTk1LDgwIDYxMCw1NSA2MjUsMTA1IDY0MCw2NSA2NTUsODAKICAgIDY3MCw4MCA2ODUsNTggNzAwLDEwMiA3MTUsNzIgNzMwLDgwIDc0NSw1MyA3NjAsMTA4IDc3NSw2MiA3OTAsODAKICAgIDgwNSw4MCA4MjAsNjAgODM1LDEwMCA4NTAsNzUgODY1LDgwIDg4MCw1NSA4OTUsMTA1IDkxMCw2NSA5MjUsODAKICAgIDk0MCw4MCA5NTUsNTggOTcwLDEwMiA5ODUsNzIgMTAwMCw4MCAxMDE1LDUzIDEwMzAsMTA4IDEwNDUsNjIgMTA2MCw4MAogICAgMTA3NSw4MCAxMDkwLDYwIDExMDUsMTAwIDExMjAsNzUgMTEzNSw4MCAxMTUwLDU1IDExNjUsMTA1IDExODAsNjUgMTIwMCw4MAogICIvPgoKICA8IS0tIEVFRyBXYXZlIChib3R0b20sIHZpb2xldCkgLS0+CiAgPHBvbHlsaW5lIGNsYXNzPSJlZWctd2F2ZS0yIiBwb2ludHM9IgogICAgMCwxNDUgMjUsMTQ1IDM1LDEzMCA1MCwxNjAgNjUsMTQwIDgwLDE0NSA5NSwxMjggMTEwLDE2MiAxMjUsMTM4IDE0MCwxNDUKICAgIDE1NSwxNDUgMTcwLDEzMiAxODUsMTU4IDIwMCwxNDIgMjE1LDE0NSAyMzAsMTI3IDI0NSwxNjMgMjYwLDEzNyAyNzUsMTQ1CiAgICAyOTAsMTQ1IDMwNSwxMzAgMzIwLDE2MCAzMzUsMTQwIDM1MCwxNDUgMzY1LDEyOCAzODAsMTYyIDM5NSwxMzggNDEwLDE0NQogICAgNDI1LDE0NSA0NDAsMTMyIDQ1NSwxNTggNDcwLDE0MiA0ODUsMTQ1IDUwMCwxMjcgNTE1LDE2MyA1MzAsMTM3IDU0NSwxNDUKICAgIDU2MCwxNDUgNTc1LDEzMCA1OTAsMTYwIDYwNSwxNDAgNjIwLDE0NSA2MzUsMTI4IDY1MCwxNjIgNjY1LDEzOCA2ODAsMTQ1CiAgICA2OTUsMTQ1IDcxMCwxMzIgNzI1LDE1OCA3NDAsMTQyIDc1NSwxNDUgNzcwLDEyNyA3ODUsMTYzIDgwMCwxMzcgODE1LDE0NQogICAgODMwLDE0NSA4NDUsMTMwIDg2MCwxNjAgODc1LDE0MCA4OTAsMTQ1IDkwNSwxMjggOTIwLDE2MiA5MzUsMTM4IDk1MCwxNDUKICAgIDk2NSwxNDUgOTgwLDEzMiA5OTUsMTU4IDEwMTAsMTQyIDEwMjUsMTQ1IDEwNDAsMTI3IDEwNTUsMTYzIDEwNzAsMTM3IDEwODUsMTQ1CiAgICAxMTAwLDE0NSAxMTE1LDEzMCAxMTMwLDE2MCAxMTQ1LDE0MCAxMTYwLDE0NSAxMTc1LDEyOCAxMTkwLDE2MiAxMjAwLDE0NQogICIvPgoKICA8IS0tIEFnZW50IDAxOiBQcmVwcm9jZXNzaW5nIC0tPgogIDxnIGNsYXNzPSJub2RlLXB1bHNlIiBmaWx0ZXI9InVybCgjZ2xvdy1jeWFuKSI+CiAgICA8cmVjdCB4PSI2MCIgeT0iMTU4IiB3aWR0aD0iMTIwIiBoZWlnaHQ9IjQ4IiByeD0iOCIgZmlsbD0iIzBEMTExNyIgc3Ryb2tlPSIjMDBGRkVBIiBzdHJva2Utd2lkdGg9IjEuNSIvPgogICAgPHRleHQgeD0iMTIwIiB5PSIxNzYiIGNsYXNzPSJub2RlLWlkIiBmaWxsPSIjMDBGRkVBIiBmb250LXNpemU9IjgiPkFHRU5UIDAxPC90ZXh0PgogICAgPHRleHQgeD0iMTIwIiB5PSIxODkiIGNsYXNzPSJub2RlLWxhYmVsIj5QcmVwcm9jZXNzaW5nPC90ZXh0PgogICAgPHRleHQgeD0iMTIwIiB5PSIyMDAiIGNsYXNzPSJub2RlLWxhYmVsIiBmaWxsPSIjNjQ3NDhCIj5JQ0EgwrcgQVNSIMK3IEZpbHRlcjwvdGV4dD4KICA8L2c+CgogIDwhLS0gQWdlbnQgMDI6IEZlYXR1cmUgRXh0cmFjdGlvbiAtLT4KICA8ZyBjbGFzcz0ibm9kZS1wdWxzZSIgZmlsdGVyPSJ1cmwoI2dsb3ctY3lhbikiIHN0eWxlPSJhbmltYXRpb24tZGVsYXk6MC40cyI+CiAgICA8cmVjdCB4PSIyNzAiIHk9IjE1OCIgd2lkdGg9IjEzMCIgaGVpZ2h0PSI0OCIgcng9IjgiIGZpbGw9IiMwRDExMTciIHN0cm9rZT0iIzAwRkZFQSIgc3Ryb2tlLXdpZHRoPSIxLjUiLz4KICAgIDx0ZXh0IHg9IjMzNSIgeT0iMTc2IiBjbGFzcz0ibm9kZS1pZCIgZmlsbD0iIzAwRkZFQSIgZm9udC1zaXplPSI4Ij5BR0VOVCAwMjwvdGV4dD4KICAgIDx0ZXh0IHg9IjMzNSIgeT0iMTg5IiBjbGFzcz0ibm9kZS1sYWJlbCI+RmVhdHVyZSBFeHRyYWN0LjwvdGV4dD4KICAgIDx0ZXh0IHg9IjMzNSIgeT0iMjAwIiBjbGFzcz0ibm9kZS1sYWJlbCIgZmlsbD0iIzY0NzQ4QiI+QmFuZCDCtyBFbnRyb3B5IMK3IFdhdmVsZXQ8L3RleHQ+CiAgPC9nPgoKICA8IS0tIEFnZW50IDAzOiBDbGFzc2lmaWNhdGlvbiAtLT4KICA8ZyBjbGFzcz0ibm9kZS1wdWxzZSIgZmlsdGVyPSJ1cmwoI2dsb3ctdmlvbGV0KSIgc3R5bGU9ImFuaW1hdGlvbi1kZWxheTowLjhzIj4KICAgIDxyZWN0IHg9IjQ5MCIgeT0iMTU4IiB3aWR0aD0iMTMwIiBoZWlnaHQ9IjQ4IiByeD0iOCIgZmlsbD0iIzBEMTExNyIgc3Ryb2tlPSIjQTg1NUY3IiBzdHJva2Utd2lkdGg9IjEuNSIvPgogICAgPHRleHQgeD0iNTU1IiB5PSIxNzYiIGNsYXNzPSJub2RlLWlkIiBmaWxsPSIjQTg1NUY3IiBmb250LXNpemU9IjgiPkFHRU5UIDAzPC90ZXh0PgogICAgPHRleHQgeD0iNTU1IiB5PSIxODkiIGNsYXNzPSJub2RlLWxhYmVsIj5DbGFzc2lmaWNhdGlvbjwvdGV4dD4KICAgIDx0ZXh0IHg9IjU1NSIgeT0iMjAwIiBjbGFzcz0ibm9kZS1sYWJlbCIgZmlsbD0iIzY0NzQ4QiI+RUVHTmV0IMK3IFRyYW5zZm9ybWVyPC90ZXh0PgogIDwvZz4KCiAgPCEtLSBBZ2VudCAwNDogRGVjaXNpb24gLS0+CiAgPGcgY2xhc3M9Im5vZGUtcHVsc2UiIGZpbHRlcj0idXJsKCNnbG93LXZpb2xldCkiIHN0eWxlPSJhbmltYXRpb24tZGVsYXk6MS4ycyI+CiAgICA8cmVjdCB4PSI3MTAiIHk9IjE1OCIgd2lkdGg9IjEyMCIgaGVpZ2h0PSI0OCIgcng9IjgiIGZpbGw9IiMwRDExMTciIHN0cm9rZT0iI0E4NTVGNyIgc3Ryb2tlLXdpZHRoPSIxLjUiLz4KICAgIDx0ZXh0IHg9Ijc3MCIgeT0iMTc2IiBjbGFzcz0ibm9kZS1pZCIgZmlsbD0iI0E4NTVGNyIgZm9udC1zaXplPSI4Ij5BR0VOVCAwNDwvdGV4dD4KICAgIDx0ZXh0IHg9Ijc3MCIgeT0iMTg5IiBjbGFzcz0ibm9kZS1sYWJlbCI+RGVjaXNpb248L3RleHQ+CiAgICA8dGV4dCB4PSI3NzAiIHk9IjIwMCIgY2xhc3M9Im5vZGUtbGFiZWwiIGZpbGw9IiM2NDc0OEIiPlJMIMK3IENvbW1hbmRzPC90ZXh0PgogIDwvZz4KCiAgPCEtLSBBZ2VudCAwNTogVmlzdWFsaXphdGlvbiAtLT4KICA8ZyBjbGFzcz0ibm9kZS1wdWxzZSIgZmlsdGVyPSJ1cmwoI2dsb3ctY3lhbikiIHN0eWxlPSJhbmltYXRpb24tZGVsYXk6MS42cyI+CiAgICA8cmVjdCB4PSI5MjAiIHk9IjE1OCIgd2lkdGg9IjEzMCIgaGVpZ2h0PSI0OCIgcng9IjgiIGZpbGw9IiMwRDExMTciIHN0cm9rZT0iIzAwRkZFQSIgc3Ryb2tlLXdpZHRoPSIxLjUiLz4KICAgIDx0ZXh0IHg9Ijk4NSIgeT0iMTc2IiBjbGFzcz0ibm9kZS1pZCIgZmlsbD0iIzAwRkZFQSIgZm9udC1zaXplPSI4Ij5BR0VOVCAwNTwvdGV4dD4KICAgIDx0ZXh0IHg9Ijk4NSIgeT0iMTg5IiBjbGFzcz0ibm9kZS1sYWJlbCI+VmlzdWFsaXphdGlvbjwvdGV4dD4KICAgIDx0ZXh0IHg9Ijk4NSIgeT0iMjAwIiBjbGFzcz0ibm9kZS1sYWJlbCIgZmlsbD0iIzY0NzQ4QiI+V2ViU29ja2V0IMK3IDMwZnBzPC90ZXh0PgogIDwvZz4KCiAgPCEtLSBDb25uZWN0b3IgbGluZXMgLS0+CiAgPGxpbmUgeDE9IjE4MCIgeTE9IjE4MiIgeDI9IjI3MCIgeTI9IjE4MiIgY2xhc3M9ImNvbm5lY3RvciIgc3Ryb2tlPSIjMDBGRkVBIi8+CiAgPGxpbmUgeDE9IjQwMCIgeTE9IjE4MiIgeDI9IjQ5MCIgeTI9IjE4MiIgY2xhc3M9ImNvbm5lY3RvciIgc3Ryb2tlPSIjMDBGRkVBIi8+CiAgPGxpbmUgeDE9IjYyMCIgeTE9IjE4MiIgeDI9IjcxMCIgeTI9IjE4MiIgY2xhc3M9ImNvbm5lY3RvciIgc3Ryb2tlPSIjQTg1NUY3Ii8+CiAgPGxpbmUgeDE9IjgzMCIgeTE9IjE4MiIgeDI9IjkyMCIgeTI9IjE4MiIgY2xhc3M9ImNvbm5lY3RvciIgc3Ryb2tlPSIjQTg1NUY3Ii8+CgogIDwhLS0gQXJyb3cgaGVhZHMgLS0+CiAgPHBvbHlnb24gcG9pbnRzPSIyNzAsMTc4IDI2MiwxODIgMjcwLDE4NiIgZmlsbD0iIzAwRkZFQSIvPgogIDxwb2x5Z29uIHBvaW50cz0iNDkwLDE3OCA0ODIsMTgyIDQ5MCwxODYiIGZpbGw9IiMwMEZGRUEiLz4KICA8cG9seWdvbiBwb2ludHM9IjcxMCwxNzggNzAyLDE4MiA3MTAsMTg2IiBmaWxsPSIjQTg1NUY3Ii8+CiAgPHBvbHlnb24gcG9pbnRzPSI5MjAsMTc4IDkxMiwxODIgOTIwLDE4NiIgZmlsbD0iI0E4NTVGNyIvPgo8L3N2Zz4K" alt="EEG-MPI Pipeline" width="100%"/>
</div>

---

<div align="center">

| ⚡ Latency | 📡 Channels | 🧠 Agents | 🎯 Accuracy | 🖥️ Dashboard |
|:---:|:---:|:---:|:---:|:---:|
| `< 50ms` | `256 ch` | `5 specialized` | `99.2%` | `30 fps` |

</div>

---

## 🧬 What is EEG-MPI?

EEG-MPI is an open-source **Multi-Agent System (MAS)** for real-time EEG signal
processing and Brain-Computer Interface (BCI) applications.
Unlike monolithic EEG pipelines, EEG-MPI distributes processing across
**5 specialized AI agents** that run in parallel, communicate via a shared
message bus, and collaboratively produce high-accuracy mental state predictions.

> **"From raw brain signal to actionable command in under 50 milliseconds."**

---

## 🤖 Agent Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                        EEG-MPI PIPELINE                         │
└─────────────────────────────────────────────────────────────────┘

 [EEG Device]
      │
      ▼
┌─────────────┐    ┌─────────────────┐    ┌──────────────────────┐
│  Agent 01   │───▶│    Agent 02     │───▶│      Agent 03        │
│Preprocessing│    │Feature Extract. │    │  Mental Classifier   │
│             │    │                 │    │                      │
│ • ICA/ASR   │    │ • Band Power    │    │ • EEGNet + Transformer│
│ • Bandpass  │    │ • Entropy       │    │ • Emotion Detection  │
│ • Artifact  │    │ • Coherence     │    │ • Fatigue / Focus    │
│   Removal   │    │ • Wavelets      │    │ • Motor Intent       │
└─────────────┘    └─────────────────┘    └──────────────────────┘
                                                     │
                   ┌────────────────┐                │
                   │   Agent 05     │◀───────────────┘
                   │ Visualization  │    ┌──────────────┐
                   │                │    │   Agent 04   │
                   │ • WebSocket    │◀───│   Decision   │
                   │ • Topography   │    │              │
                   │ • 30fps Stream │    │ • RL-based   │
                   └────────────────┘    │ • Thresholds │
                           │             │ • Commands   │
                           ▼             └──────────────┘
                     [Dashboard]              │
                                              ▼
                                        [BCI Output]
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Redis (for Message Bus)
- Compatible EEG device or sample data

### Installation

```bash
# Clone the repository
git clone https://github.com/eeg-mpi/eeg-mpi.git
cd eeg-mpi

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install EEG-MPI
pip install -e .
```

### Launch the Pipeline

```bash
# Start Redis (required for Message Bus)
redis-server

# Run with sample EEG data
python -m eegmpi --source sample --mode demo

# Run with real EEG device (e.g. OpenBCI)
python -m eegmpi --source openbci --port COM3 --channels 16

# Run with Emotiv headset
python -m eegmpi --source emotiv --mode realtime

# Launch dashboard
python -m eegmpi.dashboard --port 8080
# Open: http://localhost:8080
```

---

## 🎧 Supported EEG Devices

| Device | Channels | Sample Rate | Protocol | Status |
|--------|----------|-------------|----------|--------|
| OpenBCI Cyton | 8–16 ch | 250 Hz | Serial/BLE | ✅ Stable |
| Emotiv EPOC X | 14 ch | 256 Hz | USB/BLE | ✅ Stable |
| Muse 2 / Muse S | 4 ch | 256 Hz | BLE | ✅ Stable |
| g.tec g.USBamp | 16–64 ch | 2400 Hz | USB | ✅ Stable |
| BrainFlow (any) | Variable | Variable | LSL | ✅ Stable |
| NeuroSky MindWave | 1 ch | 512 Hz | BLE | 🔄 Beta |
| Neurosity Crown | 8 ch | 256 Hz | WiFi | 🔄 Beta |
| Any LSL device | Variable | Variable | LSL | ✅ Stable |

---

## 🧩 Agent API

All agents extend `BaseAgent` and implement a standard interface:

```python
from eegmpi.agents import BaseAgent

class CustomAgent(BaseAgent):
    agent_id = "custom_agent_07"
    subscribe_to = ["feature_extraction.output"]
    publish_to   = "custom_agent.output"

    async def process(self, payload: dict) -> dict:
        # Your processing logic here
        data = payload["data"]
        result = self.run_model(data)
        return {"prediction": result, "confidence": 0.97}
```

### Built-in Agents

```python
from eegmpi.agents import (
    PreprocessingAgent,      # Agent 01 — Noise removal, ICA, ASR
    FeatureExtractionAgent,  # Agent 02 — Band power, entropy, wavelets
    ClassificationAgent,     # Agent 03 — EEGNet + Transformer ensemble
    DecisionAgent,           # Agent 04 — RL-based command generation
    VisualizationAgent,      # Agent 05 — Real-time WebSocket dashboard
)
```

---

## ⚙️ Configuration (`config.yaml`)

```yaml
eegmpi:
  version: "2.4.1"
  mode: realtime           # realtime | offline | demo

source:
  device: openbci          # openbci | emotiv | muse | brainflow | lsl | sample
  channels: 16
  sample_rate: 250         # Hz
  buffer_size: 512         # samples

message_bus:
  backend: redis
  host: localhost
  port: 6379

agents:
  preprocessing:
    enabled: true
    bandpass: [1, 50]      # Hz
    notch: 50              # Hz (or 60 for US)
    ica: true
    asr: true

  feature_extraction:
    enabled: true
    bands:
      delta:  [1, 4]
      theta:  [4, 8]
      alpha:  [8, 13]
      beta:   [13, 30]
      gamma:  [30, 50]
    entropy: true
    coherence: true
    wavelet: true

  classification:
    enabled: true
    model: eegnet_transformer
    targets: [emotion, focus, fatigue, motor_intent]
    confidence_threshold: 0.85

  decision:
    enabled: true
    strategy: rl_based     # rl_based | rule_based | hybrid
    action_space: [command_left, command_right, command_select, idle]

  visualization:
    enabled: true
    port: 8080
    fps: 30
    show_topography: true
    show_spectrum: true

logging:
  level: INFO
  output: [console, file]
  file: logs/eegmpi.log
```

---

## 🛠️ Tech Stack

<div align="center">

![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![WebSocket](https://img.shields.io/badge/WebSocket-010101?style=for-the-badge&logo=socketdotio&logoColor=white)
![MNE](https://img.shields.io/badge/MNE--Python-00457C?style=for-the-badge&logo=python&logoColor=white)

</div>

| Layer | Technology |
|-------|-----------|
| Signal Processing | MNE-Python, SciPy, NumPy |
| Deep Learning | PyTorch, EEGNet, Transformer |
| Message Bus | Redis Pub/Sub, asyncio |
| API Server | FastAPI, Uvicorn |
| Dashboard | WebSocket, Vanilla JS, Canvas API |
| Device Protocol | BrainFlow, LSL, BLE, Serial |
| Testing | pytest, pytest-asyncio |
| CI/CD | GitHub Actions |

---

## 🤝 Contributing

We welcome contributions! Read [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

### Ways to Contribute
- 🐛 **Bug reports** — Open an [Issue](https://github.com/eeg-mpi/eeg-mpi/issues)
- 💡 **Feature ideas** — Start a [Discussion](https://github.com/eeg-mpi/eeg-mpi/discussions)
- 🧠 **New Agent** — Implement a new agent following the `BaseAgent` interface
- 📖 **Documentation** — Improve docs in the `/docs` folder
- 🧪 **Tests** — Add test coverage for existing agents

### Development Setup

```bash
git clone https://github.com/eeg-mpi/eeg-mpi.git
cd eeg-mpi
pip install -e ".[dev]"
pre-commit install
pytest tests/
```

---

<div align="center">

**Built for the neuroscience and BCI community.**

[![Follow on X](https://img.shields.io/badge/Follow_@eeg__mpi-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/eeg_mpi)
[![Star this repo](https://img.shields.io/badge/⭐_Star_this_repo-yellow?style=for-the-badge)](https://github.com/eeg-mpi/eeg-mpi)

© 2025 EEG-MPI · MIT License · Made with 🧠 and ⚡

</div>

