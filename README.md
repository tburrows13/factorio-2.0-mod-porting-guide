Porting a 1.1 mod to 2.0 is _hard work_. Many changes have occured, and whilst the 2.0 docs are in a good state, there is no comphrehensive documentation detailing how each thing has _changed_. This guide won't explain every change, but it will hopefully set you up to discover how to make the changes yourself.

\- Xorimuth
# Table of Contents
1. [Important links](#Important-links)
2. [Steps](#Steps)
3. [When you reach an error](#When-you-reach-an-error)
4. [Notable changes](#Notable-changes)
5. [Advanced tools](#Advanced-tools)

# Important links
- [2.0 changelog](https://github.com/tburrows13/factorio-2.0-mod-porting-guide/blob/master/2.0-changelog-filtered.md) - Especially the sections __Modding__ (for prototype/data stage) and __Scripting__ (for runtime/control stage).
- [2.0 docs](https://lua-api.factorio.com/latest/) - The docs detail the exact specification for everything in 2.0.
- [1.1 docs](https://lua-api.factorio.com/1.1.110/) - The 1.1 docs are still useful! If you come across a part of your mod that isn't working in 2.0, refer to the 1.1 docs to see how it used to work, and then maybe that will help you find similar functionality in the 2.0 docs.
- [Base & Core mod changes](https://github.com/wube/factorio-data/commit/7522d3763e76e09ce1a46cba676dfc2b6d12b127) - A lot of the changes in 2.0 aren't in the docs at all, because they are changes in __base__ and __core__ 'mods'. This (large!) diff shows all the changes to these 'mods'.
- [Application directory](https://wiki.factorio.com/Application_directory#Application_directory) - Explains how to access `./data`, which contains __base__ and __core__ mods that you already have as part of your installation. Open `./data` in VSCode and use "Find in files" (Ctrl+Shift+F) to search through them. I've also found the 1.1 data files useful when porting - you can download them from the [factorio-data repo](https://github.com/wube/factorio-data/tree/1.1.110).
- [VSCode Factorio Modding Tool Kit](https://marketplace.visualstudio.com/items?itemName=justarandomgeek.factoriomod-debug) and [Setup video](https://youtu.be/oNfMNFxy2X4) - This isn't essential, but it can help a lot if you're familiar with debuggers. To enable the debugger in data stage, use the "(Settings & Data)" debug preset. Even if you don't install it for the debugger, once set up it will start pointing out things that you've done wrong, which is a sign that that thing might have changed in 2.0. For some changed functions, fmtk will even mark them as deprecated by crossing them out - hovering over them will tell you which functions to change to.

# Steps

## 1. Disable space-age, quality, and elevated-rails, and any other mods
Make sure your mod loads with base game first. If you have these expansion 'mods' loaded when trying to port your mod, **they will get in the way.** In particular, quality mod expects your recipes to be correctly defined. If you are coming from a 1.1 mod, they almost certainly won't be. Instead of the game giving you helpful error messages, quality mod will give you unhelpful error messages.

## 2. Read through the 2.0 changelog
Yes, it is long. No, you don't have to remember everything. Take note of anything that you think might be relevant for your mod. Later on, you'll come back here to Control+F for other things, but having a rough idea of what you might need to change will help.

## 3. Update info.json
```diff
-  "factorio_version": "1.1",
+  "factorio_version": "2.0",
```

## 4. Make changes based on 2.0 changelog (optional)
If you've noticed things in the changelog that you _know_ you'll have to change, you may as well do that now. Also see [Notable changes](#Notable-changes).

## 5. Try to load your mod in 2.0
Here's the long process. Enable your mod, reach an error, fix the error, reload the game, reach another error, fix the error, and so on until you reach the main menu.

## 6. Load a game
Now that you've reached the main menu, start a new game with your mod, play around with it, or load an existing save. Fix any errors as they come up. You can Control+Click on "Single player" in the main menu to quickly enter a testing world, then run `/cheat all`. Install [Editor Extensions](https://mods.factorio.com/mod/EditorExtensions) if you want the test world to be immediately populated by cheat tooling.

## 7. Clean up loose ends
From the main menu, Control+Alt+Click on "Settings". Then click on "The rest" and enable "check-unused-prototype-data". Reload your game, and check `factorio-current.log`. You will likely log lines like this:
```
   3.744 Warning PrototypeLoader.cpp:199: Value ROOT.shortcut.spidertron-enhancements-recall-shortcut.icon_mipmaps was not used.
```
These warnings tell you which prototype properties aren't being loaded. This may point to further things you need to change, or just tell you about things that are no longer necessary and you can safely delete (e.g. `icon_mipmaps` is no longer needed anywhere).

## 8. 2.0 polish
Now that your mod is fully functional, read https://github.com/tburrows13/factorio-2.0-mod-porting-guide/blob/master/utilising-2.0-features.md for ways to make your mod fit better into 2.0/Space Age.

# When you reach an error
If you reach errors in prototype-stage lua execution, it is probably because something has changed or been removed in __base__/__core__.

If you reach "Error while loading ..." errors, it is probably because something has changed in the prototype-stage API specification.

If you encounter errors while playing ingame, it is probably because something has changed in the runtime-stage API specification.

1. Find the relevant section of code in your mod, and work out what it is trying to do.
2. Search (Control+F) [the changelog](https://forums.factorio.com/116184) to see if there's any changes mentioned in this area.
3. Search [the docs](https://lua-api.factorio.com/latest/) and ensure that what you are doing matches exactly with what the docs are expecting.
4. Search (Control+Shift+F) in `./data` to see if there's any references to this thing in __base__/__core__. This might give you examples as to how it is now used.
5. Still stuck? You can try searching the 1.1 docs or the 1.1 `./data` directory to see how things used to be. This might give you some more clues on where it went, or what to search for in the changelog.

# Notable changes
These are things that pretty much every mod will have to change, so you may as well change them before trying to load your mod.

## Prototype stage

### Recipes
[Recipes](https://lua-api.factorio.com/latest/prototypes/RecipePrototype.html) have undergone many changes. In 1.1, there were lots of allowed formats. In 2.0, there is pretty much only one valid format for each thing.

Entries in [ingredients](https://lua-api.factorio.com/latest/prototypes/RecipePrototype.html#ingredients) and [results](https://lua-api.factorio.com/latest/prototypes/RecipePrototype.html#results) tables may no longer use the shorthand `{"steel-plate, 100"}` and must now use the longhand `{type="item", name="steel-plate", amount=100}`.

Furthermore, `result` and `result_count` are no longer valid. All results must be specified using the full `results = {{type="item", name="chemical-plant", amount=1}}`.

Example:
```diff
-{
-  type = "recipe",
-  name = "po-interface",
-  enabled = false,
-  ingredients =
-  {
-    {"steel-plate", 100},
-    {"processing-unit", 50},
-  },
-  result = "po-interface",
-  result_count = 1,
-}
+{
+  type = "recipe",
+  name = "po-interface",
+  enabled = false,
+  ingredients =
+  {
+    {type="item", name="steel-plate", amount=100},
+    {type="item", name="processing-unit", amount=50},
+  },
+  results = {
+    {type="item", name="po-interface", amount = 1}
+  },
+}
```

In 1.1, recipes could also define `normal` and `expensive` variations. In 2.0, this is no longer supported, instead everything must be defined in the recipe base.

### hr_version
In 1.1, most graphics definitions would define a standard definition and a high-res definition version of each thing. In 2.0, only the high-res version should be defined, and if the user sets "Sprite resolution" to "Medium", then the graphics will be automatically downscaled on startup. (If `scale` is **greater than** `0.5`, the sprite will never be downscaled).

```diff
-{
-  filename = "__base__/graphics/entity/artillery-turret/artillery-turret-base.png",
-  height = 100,
-  width = 104,
-  priority = "high",
-  scale = 1,
-  hr_version = {
-    filename = "__base__/graphics/entity/artillery-turret/hr-artillery-turret-base.png",
-    height = 200,
-    width = 208,
-    priority = "high",
-    scale = 0.5,
-  },
-},
+{
+  filename = "__base__/graphics/entity/artillery-turret/hr-artillery-turret-base.png",
+  height = 200,
+  width = 208,
+  priority = "high",
+  scale = 0.5,
+}
```

### Circuit connector definitions
Replace `circuit_connector_definitions.create_single` with `circuit_connector_definitions.create_vector`?

TODO?

### Module specifications
TODO?

### Crafting machine graphics
In 1.1, `animations` and `working_visualisations` were set on the prototype directly. In 2.0, they are inside [`graphics_set`](https://lua-api.factorio.com/latest/prototypes/CraftingMachinePrototype.html#graphics_set).

### Collision masks
[Collision layers](https://lua-api.factorio.com/latest/prototypes/CollisionLayerPrototype.html) are now prototypes rather than hardcoded strings. See `base/prototypes/collision-layers.lua` for a list of layers defined by base mod. [CollisionMaskConnector](https://lua-api.factorio.com/latest/types/CollisionMaskConnector.html) docs explain how to use them.

### Hidden flag
`"hidden"` is no longer a flag, and is now a [property](https://lua-api.factorio.com/latest/prototypes/PrototypeBase.html#hidden) of every single prototype.

```diff
-my_prototype.flags = {"hidden"}
+my_prototype.hidden = true
```

### Fluidboxes and pipe connections
Fluidbox `base_area`, `base_level`, and `height` have all been replaced by just `volume`, which should be set equal to `base_area × height × 100`. If you were using `base_level` to control whether fluids can flow in/out, ensure `flow_direction` on each pipe connection is set correctly instead.
In `pipe_connections`, `type` has been renamed to `flow_direction`, connection direction must be specified in `direction`, and connection positions should be reduced by 1 in the direction that the pipe connection is facing.

## Runtime stage
### global -> storage
In 1.1, `global` was used to store mod data in between save/loads. In 2.0, it has been renamed to [`storage`](https://lua-api.factorio.com/latest/auxiliary/storage.html).

### GUI styles changes
If you were relying on any styles defined by __core__, they have probably changed or been removed. Refer to 2.0's style.lua and the 1.1's style.lua (or the diff on github) to try and find appropriate replacements. Or just copy the styles you were using from 1.1's style.lua into your own mod.

### Script rendering
Script [rendering](https://lua-api.factorio.com/latest/classes/LuaRendering.html) is now done by manipulating [render-objects](https://lua-api.factorio.com/latest/classes/LuaRenderObject.html) directly rather than by ID. You can use [`rendering.get_object_by_id(my_id)`](https://lua-api.factorio.com/latest/classes/LuaRendering.html#get_object_by_id) to convert IDs to objects in migrations.

### Logistic points
Logistic requests are now handled through [Logistic Points](https://lua-api.factorio.com/latest/classes/LuaLogisticPoint.html), accessible from the entity via [`get_logistic_point`](https://lua-api.factorio.com/latest/classes/LuaEntity.html#get_logistic_point).

TODO

### Wire connections and control behaviours
See [this commit](https://github.com/RedRafe/solar-productivity/commit/f8c15f7caaec18e89e87f3956b27762e939b7d7b) for some examples of changes to `circuit_connection_definitions`, `connect_neighbour`, and `get_control_behavior`

### on_entity_destroyed -> on_object_destroyed
And associated `event.unit_number` -> `event.useful_id`.

### Quality in item stacks
Especially `get_contents`. TODO

### Remote view
Replace `player.open_map(new_position)` or `player.zoom_to_world(new_position)` with `player.set_controller({type = defines.controllers.remote, position = new_position})`. Currently `player.close_map()` has no replacement, and there is no way to set the zoom level.
When in remote view, a player's `position`, `surface`, etc will be the position that they are currently viewing. To get their _character's_ position, use [`player.physical_position`](https://lua-api.factorio.com/latest/classes/LuaPlayer.html#physical_position), `physical_surface`, etc instead.

# Advanced tools
If you have a _lot_ of prototype-stage definitions to convert, you may find the following helpful. Please don't use them unless you have everything backed up using git, and they should be used with careful hand-holding.

## Regex find-replaces
![Screenshot 2024-10-22 at 02 17 41](https://gist.github.com/user-attachments/assets/cd9e8216-43f7-4088-a039-dafd38fe98da)


### Convert result+result_count to results

Find: `(\s\s+)result = (.*),\n.*result_count = (.*),`

Replace: `$1results = {{type="item", name=$2, amount=$3}},`

Then convert result by itself to results
(careful not to mess with minable, place_as_tile)

Find: `(\s\s+)result = (.*),`

Replace: `$1results = {{type="item", name=$2, amount=1}},`

### Convert shorthand to longhand in ingredients/results
(careful, don’t apply to tech `unit` or localised-strings)

Find: `\{"(.*)",\s*(\d+)\}`

Replace: `{type="item", name="$1", amount=$2}`

### Fluidboxes
Volume calculated from `base_area*height*100`. Re-run the find-replace for each combination of area/height you find.

Find: `\s*base_area = 10,(\s*)height = 1,`

Replace: `\n$1volume = 1000,`

### Pipe connections
Requires manually changing direction and position afterwards. Position should be reduced by 1 in the direction it is facing.

Find: `(\{\s?)type(\s?=\s?".*")(,\s?)position`

Replace: `$1flow_direction$2, direction = defines.direction.north, position`

## Python scripts
### Remove hr_version
`remove_hr_version.py` removes all standard-resolution definitions from your code, replacing them with the contents of `hr_version`, and then deleting `hr_version`.

Caveats:
- only works if your graphics definitions are correctly indented
- only works if your files use spaces rather than tabs (use VSCode regex find-replace `\t` -> `  ` to fix)
- doesn't work correctly on sprite prototypes (`type = "sprite"`)

### Rename/delete graphics files
`delete_files_with_hr_version.py` deletes all files where there is also a file with hr- existing in the same folder.
`rename_hr_files.py` renames files, removing hr- from their names.

Run them in that order. Why 2 separate steps? Do a commit in between and git will realise that it is a deletion and rename, rather than a file-change and deletion. 
