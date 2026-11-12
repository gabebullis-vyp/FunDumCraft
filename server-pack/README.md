# Running FunDumCraft on a server

The Prism instance in this repo is a **client** pack. If you drop its mods folder straight onto a server, it crashes within a second, before Minecraft even writes a log. That's because some of these mods only work on a PC with a screen and graphics card.

This folder builds a server copy that leaves those mods out.

## Why the server was crashing

1. **Client-only mods.** Sodium dies in the very first second of startup, before logging exists, which is why the host showed no log at all. Behind it, Immersive Damage Indicators, Cubes Without Borders, Animated Hearts and MC2 Interactive Foliage each crash a server too. Those 5, plus about 30 other client-only mods (shaders, sounds, UI tweaks), are listed in `client-only-mods.txt`. Players keep all of them on their PCs.
2. **Improved Mobs 1.16 vs Cataclysm.** Improved Mobs 1.16 builds a copy of every mob at startup inside a fake world that pretends to be the client. Cataclysm's bosses then touch a client-only field, and a real server doesn't have it. The server stops with "Failed to load datapacks, can't proceed with server load". So the pack now uses **Improved Mobs 1.15.2 + TenshiLib 2.2.5**, and the config carries over all the same settings. **Don't update either one** until Improved Mobs fixes this.

## Build the server files

Needs Python 3.10 or newer. From the repo root:

```
python server-pack/make_server_pack.py ../FunDumCraft-server --zip
```

That writes `../FunDumCraft-server/` and `../FunDumCraft-server.zip` containing `mods`, `config`, `defaultconfigs`, `kubejs` and `datapacks`.

If it prints a WARNING about a jar in the list that it can't find, a client-only mod was updated and renamed. Put the new file name in `client-only-mods.txt`.

## Set up the server (Apex Hosting)

1. **Loader:** NeoForge for Minecraft 1.21.1. Match the client's NeoForge build, which is **21.1.259** (see `mmc-pack.json`).
2. **Java:** set Java 21 in the Customizations tab. NeoForge 1.21.1 won't start on 17.
3. **RAM:** at least 12 GB. Tested idle with nobody online, it sits around 6 GB. Go 14 to 16 GB if 5+ people play or you build big Create machines.
4. Stop the server. Delete the old `mods`, `config`, `defaultconfigs`, `kubejs` and `datapacks` folders on it.
5. Upload `FunDumCraft-server.zip` over FTP, then use Extract Here in the file manager.
6. Start it. The first boot builds a new world and takes a few minutes. Look for `Done (` in the console.

If Apex's NeoForge dropdown doesn't list 21.1.259, Apex supports uploading a custom server jar. NeoForge's official ServerStarterJar (github.com/neoforged/ServerStarterJar) can be used as that jar to install an exact build. We haven't tested that route yet.

## When you add or update mods

If a new mod is purely visual (shaders, HUD, sounds, menus, animations), add its jar name to `client-only-mods.txt`. If the server crashes after an update, check `crash-reports/` first, then `logs/latest.log`. A line saying `invalid dist DEDICATED_SERVER` names the client-only mod to add to the list.
