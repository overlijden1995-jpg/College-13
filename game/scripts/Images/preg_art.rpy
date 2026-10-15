# ============================================================
# PREGNANCY ART — single registry of the art that changes with the visual pregnancy stage
# ============================================================
#
# Visual stage = pregnancy_visual_stage(girl) (pregnancy.rpy): 0 normal art, 1 small bump + bigger
# breasts, 2 full belly. Full mode only.
#
# The files live in images/characters/<Girl>/<Pose>/Preg/, under the ARTIST'S own names (a re-export
# drops in without renaming):
#   "...XL"   fits the bigger breasts (stage 1 on)
#   "...Preg" fits the belly
#
# PREG_ART[gid][original file] = {stage: variant file}, both relative to images/characters/<Girl>/.
#   {1: x}         x from stage 1 on (a stage with no entry inherits the closest one below it)
#   {2: y}         the original at stage 1, y at stage 2
#   {1: x, 2: y}   x at stage 1, y at stage 2
# A key starting with "+" is an ADDED layer with no original: nothing is drawn below its first stage.
# A variant None HIDES the layer from that stage: the variant art of another layer already draws it (Shion's
# Cowgirl nipples are baked into her XL chest).
#
# To give a layer pregnancy art:
#   1. drop the file in <Pose>/Preg/
#   2. add the pair here
#   3. in the character's layeredimage / image, write preg_art("gid", "Pose/File.png") where the
#      original path was
#   A belly overlay ("+" key) of a scene where she rides (Cowgirl, Full Nelson) goes in as preg_belly(...)
#   instead of preg_art(...): same art, plus a little motion of its own (PREG_BELLY_MOTION, below).
# Nothing else changes: scenes, previews and menus show the image by name, the Cores are untouched.
# One exception: _FN_CHEST_UP_MAPS (Core_FullNelson.rpy) holds the art paths of the pulled-up Full
# Nelson tops, so those four entries call preg_art() there.
# Poses with no entry (Doggy, Reverse Cowgirl, Laying Down...) keep the normal art.
#
# What stays OUT of the game folder: the darker-areola art (the "Darker" folders, and the files that
# bake it in under a "Preg" name: Rogue's "... Chest Preg", Tenny's "ChestPreg", NTW's HJ "BoobsPreg").
# It is a placeholder, never shown for now. When the final art comes: an added layer right above the
# chest, below the chest clothing, with a pierced variant.
#
# A garment that COVERS the chest / belly needs its own XL / Preg art: over the bigger breasts and the
# belly, the normal file lets skin stick out of its outline. Every covering garment has it today. The
# art of a covering garment is drawn to sit ON the pregnancy layers (it may count on their outline),
# so the chest and the belly stay drawn under it.
#
# Console: preg_art_preview(Gwen, 2) shows a stage right now, preg_art_preview(Gwen) goes back to her
# real state. The checks of _preg_art_validate() (missing file, unwired entry, variant of another size
# than its original) run on every launch and report to log.txt.
# ============================================================

init -5 python:

    PREG_ART = {
        "gwen": {
            # ---------- Standing ----------
            "Standing/Gwen_Torso.png":                                          {1: "Standing/Preg/Gwen_Torso_Preg.png"},
            "+Standing/belly":                                                  {2: "Standing/Preg/Gwen_Torso_Preg2.png"},
            "Standing/Gwen_Chest.png":                                          {1: "Standing/Preg/Gwen_Chest_XL.png"},
            "Standing/Gwen_Chest_Piercing.png":                                 {1: "Standing/Preg/Gwen_Chest_Peirced_XL.png"},
            # trimmed where the full belly passes in front of the forearm
            "Standing/Gwen Arm Right 4.png":                                    {2: "Standing/Preg/Gwen Arm Right 4Preg.png"},
            "Standing/Clothes/Legs/Blue Skirt/Blue Skirt.png":                  {2: "Standing/Preg/Blue Skirt Preg.png"},
            "Standing/Clothes/Legs/Blue Skirt/Blue Skirt Up.png":               {2: "Standing/Preg/Blue Skirt Up Preg.png"},
            "Standing/Clothes/Chest/Corset/Cover.png":                          {1: "Standing/Preg/CoverXL.png", 2: "Standing/Preg/CoverPreg.png"},
            "Standing/Clothes/Chest/Corset/Base.png":                           {2: "Standing/Preg/BasePreg.png"},
            "Standing/Clothes/Chest/Black Bikini Top/Black Bikini Top.png":     {1: "Standing/Preg/Black Bikini TopXL.png"},
            "Standing/Clothes/Chest/Black Bikini Top/Black bikini top Up.png":  {1: "Standing/Preg/Black bikini top UpXL.png"},
            "Standing/Clothes/Gwen Towel.png":                                  {1: "Standing/Preg/Gwen TowelXL.png", 2: "Standing/Preg/Gwen TowelPreg.png"},
            # panties cut lower, under the full belly (the purple pair came under the ORIGINAL file names)
            "Standing/Clothes/Panties/Purple Panties/Purple Panties.png":       {2: "Standing/Preg/Purple Panties.png"},
            "Standing/Clothes/Panties/Purple Panties/Purple Panties Side.png":  {2: "Standing/Preg/Purple Panties Side.png"},
            "Standing/Clothes/Panties/Black Bikini Bottom/Black Bikini Panties.png":      {2: "Standing/Preg/Black Bikini PantiesPreg.png"},
            "Standing/Clothes/Panties/Black Bikini Bottom/Black bikini panties Side.png": {2: "Standing/Preg/Black bikini panties SidePreg.png"},

            # ---------- Blowjob (seen from above: the belly is part of the legs layer) ----------
            # One belly only: stages 1 and 2 look the same here (author's call), the skirt follows the legs.
            "Blowjob/Legs.png":                                                 {1: "Blowjob/Preg/LegsPreg.png"},
            "Blowjob/Clothes/Legs/Blue Skirt/Blue Skirt.png":                   {1: "Blowjob/Preg/Blue SkirtPreg.png"},
            "Blowjob/Gwen Chest.png":                                           {1: "Blowjob/Preg/Gwen ChestXL.png"},
            "Blowjob/Gwen Chest Piercings.png":                                 {1: "Blowjob/Preg/Gwen Chest PiercingsXL.png"},
            "Blowjob/Clothes/Chest/Corset/Cover.png":                           {1: "Blowjob/Preg/CoverXL.png"},
            "Blowjob/Clothes/Chest/Black Bikini Top/Black bikini Top.png":      {1: "Blowjob/Preg/Black bikini TopXL.png"},
            "Blowjob/Clothes/Chest/Black Bikini Top/Black bikini Top Up.png":   {1: "Blowjob/Preg/Black bikini Top UpXL.png"},

            # ---------- Handjob (the belly only shows at the bottom edge of the frame) ----------
            # One belly only: stages 1 and 2 look the same here too.
            "Handjob/Torso Head.png":                                           {1: "Handjob/Preg/Torso HeadPreg.png"},
            "Handjob/Torso 2.png":                                              {1: "Handjob/Preg/Torso 2Preg.png"},
            "Handjob/Gwen Chest.png":                                           {1: "Handjob/Preg/Gwen ChestXL.png"},
            "Handjob/Gwen Chest Piercing.png":                                  {1: "Handjob/Preg/Gwen Chest PiercingXL.png"},
            "Handjob/Clothes/Chest/Corset/Cover.png":                           {1: "Handjob/Preg/CoverXL.png"},
            "Handjob/Clothes/Chest/Corset/Base.png":                            {1: "Handjob/Preg/BasePreg.png"},
            "Handjob/Clothes/Chest/Black Bikini Top/Black bikini Top.png":      {1: "Handjob/Preg/Black bikini TopXL.png"},
            "Handjob/Clothes/Chest/Black Bikini Top/Black bikini Top Up.png":   {1: "Handjob/Preg/Black bikini Top UpXL.png"},

            # ---------- Titjob (no belly in frame) ----------
            # "Black BikiniXL" = the fixed straps, redrawn thicker to meet the XL cups (it replaced the first
            # "Black Bikini FixedXL"). It and "Black Bikini TopXL" were delivered inside the NTW folder.
            "Titjob/Gwen TJ Base Boobs.png":                                    {1: "Titjob/Preg/Gwen TJ Base BoobsXL.png"},
            "Titjob/Gwen TJ Nipples.png":                                       {1: "Titjob/Preg/Gwen TJ NipplesXL.png"},
            "Titjob/Gwen TJ Nipples Piercings.png":                             {1: "Titjob/Preg/Gwen TJ Nipples PiercingsXL.png"},
            "Titjob/Clothes/Chest/Black Bikini Top/Black Bikini Fixed.png":     {1: "Titjob/Preg/Black BikiniXL.png"},
            "Titjob/Clothes/Chest/Black Bikini Top/Black bikini Top.png":       {1: "Titjob/Preg/Black Bikini TopXL.png"},
            "Titjob/Clothes/Chest/Black Bikini Top/Black bikini Top Up.png":    {1: "Titjob/Preg/Black bikini Top UpXL.png"},

            # ---------- Cowgirl (also the masturbation scene) ----------
            "Cowgirl/Gwen Cowgirl Torso.png":                                   {1: "Cowgirl/Preg/Gwen Cowgirl Torso Preg.png"},
            "+Cowgirl/belly":                                                   {2: "Cowgirl/Preg/Preg Belly.png"},
            "Cowgirl/Gwen Cowgirl Boobs Base.png":                              {1: "Cowgirl/Preg/Gwen Cowgirl Boobs BaseXL.png"},
            "Cowgirl/Gwen Cowgirl Nipples.png":                                 {1: "Cowgirl/Preg/Gwen Cowgirl NipplesXL.png"},
            "Cowgirl/Gwen Cowgirl Nipples Piercings.png":                       {1: "Cowgirl/Preg/Gwen Cowgirl Nipples PiercedXL.png"},
            "Cowgirl/Clothes/Chest/Corset/Cover.png":                           {1: "Cowgirl/Preg/CoverXL.png"},
            "Cowgirl/Clothes/Chest/Corset/Base.png":                            {1: "Cowgirl/Preg/BaseXL.png", 2: "Cowgirl/Preg/BasePreg.png"},
            "Cowgirl/Clothes/Chest/Black Bikini Top/Black bikini Top.png":      {1: "Cowgirl/Preg/Black bikini TopXL.png"},
            "Cowgirl/Clothes/Chest/Black Bikini Top/Black bikini Top Up.png":   {1: "Cowgirl/Preg/Black bikini Top UpXL.png"},
        },

        "rogue": {
            # ---------- Standing ----------
            # Whole torso with the small bump from stage 1 on (it replaced the first "Preg" belly patch); the
            # full belly is an overlay right above it, like the other girls.
            "Standing/Rogue_Torso.png":                                         {1: "Standing/Preg/Rogue_TorsoPreg.png"},
            "+Standing/belly":                                                  {2: "Standing/Preg/Preg2.png"},
            "Standing/Rogue_Chest.png":                                         {1: "Standing/Preg/Rogue_Chest_XL.png"},
            "Standing/Boobs Piercing.png":                                      {1: "Standing/Preg/Boobs Piercing XL.png"},
            "Standing/Rogue Arm Right 4.png":                                   {2: "Standing/Preg/Rogue Arm Right 4Preg.png"},
            "Standing/Clothes/Legs/Black Skirt/Black Skirt.png":                {2: "Standing/Preg/Black Skirt Preg.png"},
            "Standing/Clothes/Legs/Black Skirt/Black Skirt Up.png":             {2: "Standing/Preg/Black Skirt Preg Up Preg.png"},
            # bikini bottom cut lower, under the full belly. Her green panties need no variant (they already
            # sit below the belly): the pair that came with the pregnancy art only follows the crotch tweak of
            # the new torsos, so it REPLACED the default files.
            "Standing/Clothes/Panties/Green Bikini Bottom/Green Bikini Bottom Up.png":   {2: "Standing/Preg/Green Bikini Bottom UpPreg.png"},
            "Standing/Clothes/Panties/Green Bikini Bottom/Green Bikini Bottom Side.png": {2: "Standing/Preg/Green Bikini Bottom SidePreg.png"},
            # one variant only, and the original does not close over the bigger breasts: stage 1 on
            "Standing/Clothes/Chest/Crop Top/Base.png":                         {2: "Standing/Preg/Base Preg.png"},
            "Standing/Clothes/Chest/Crop Top/Cover.png":                        {1: "Standing/Preg/Cover Preg.png"},
            "Standing/Clothes/Chest/Green Bikini Top/Green Bikini Top.png":     {1: "Standing/Preg/Green Bikini Top Preg.png"},
            "Standing/Clothes/Chest/Green Bikini Top/Green Bikini Top Up.png":  {1: "Standing/Preg/Green Bikini Top Up Preg.png"},
            # the mesh hem is cut around the full belly
            "Standing/Clothes/Over/Green Mesh/Rogue Arm 1 Mesh Top.png":        {2: "Standing/Preg/Rogue Arm 1 Mesh Top Preg.png"},
            "Standing/Clothes/Over/Green Mesh/Mesh Top 2.png":                  {2: "Standing/Preg/Mesh Top 2 Preg.png"},
            "Standing/Clothes/Over/Green Mesh/Mesh Top 3.png":                  {2: "Standing/Preg/Mesh Top 3 Preg.png"},
            "Standing/Clothes/Over/Green Mesh/Mesh Top 4.png":                  {2: "Standing/Preg/Mesh Top 4 Preg.png"},
            "Standing/Clothes/Rogue Towel.png":                                 {1: "Standing/Preg/Rogue TowelXL.png", 2: "Standing/Preg/Rogue TowelPreg2.png"},

            # ---------- Blowjob (one belly: stages 1 and 2 look the same) ----------
            "Blowjob/Legs.png":                                                 {1: "Blowjob/Preg/Legs Preg.png"},
            "Blowjob/Clothes/Legs/Rogue BJ Skirt.png":                          {1: "Blowjob/Preg/Rogue BJ Skirt Preg.png"},
            "Blowjob/Rogue Chest.png":                                          {1: "Blowjob/Preg/Rogue Chest XL.png"},
            "Blowjob/Rogue Chest Piercing.png":                                 {1: "Blowjob/Preg/Rogue Chest Piercing XL.png"},
            "Blowjob/Clothes/Chest/Crop Top/Crop Top.png":                      {1: "Blowjob/Preg/Crop Top XL.png"},
            "Blowjob/Clothes/Chest/Green Bikini Top/Rogue BJ Green Bikini Top.png":     {1: "Blowjob/Preg/Rogue BJ Green Bikini Top XL.png"},
            "Blowjob/Clothes/Chest/Green Bikini Top/Rogue BJ Green Bikini Top Up.png":  {1: "Blowjob/Preg/Rogue BJ Green Bikini Top Up XL.png"},
            "Blowjob/Clothes/Over/Mesh Top/BJ Body.png":                        {1: "Blowjob/Preg/BJ BodyPreg.png"},
            "Blowjob/Clothes/Over/Mesh Top/BJ Torso.png":                       {1: "Blowjob/Preg/BJ Torso Preg.png"},
            "Blowjob/Clothes/Over/Mesh Top/BJ Torso 3 Mesh Top.png":            {1: "Blowjob/Preg/BJ Torso 3 Mesh Top Preg.png"},

            # ---------- Handjob (one belly) ----------
            "Handjob/Torso Head.png":                                           {1: "Handjob/Preg/Torso Head Preg.png"},
            "Handjob/Torso 2.png":                                              {1: "Handjob/Preg/Torso 2 Preg.png"},
            "Handjob/Rogue Chest.png":                                          {1: "Handjob/Preg/Rogue Chest XL.png"},
            "Handjob/Boobs Piercing.png":                                       {1: "Handjob/Preg/Boobs Piercing XL.png"},
            "Handjob/Clothes/Chest/Top Crop.png":                               {1: "Handjob/Preg/Top Crop Preg.png"},
            "Handjob/Clothes/Chest/Top Crop Up.png":                            {1: "Handjob/Preg/Top Crop Up Preg.png"},
            "Handjob/Clothes/Chest/Green Bikini/Green Bikini Top Down.png":     {1: "Handjob/Preg/Green Bikini Top Down Preg.png"},
            "Handjob/Clothes/Chest/Green Bikini/Green Bikini Top Up.png":       {1: "Handjob/Preg/Green Bikini Top Up Preg.png"},

            # ---------- Titjob (no belly in frame) ----------
            # No XL "Green Bikini Top Up": the original sits above the breasts and still lines up.
            "Titjob/Rogue TJ Base Boobs.png":                                   {1: "Titjob/Preg/Rogue TJ Base BoobsXL.png"},
            "Titjob/Rogue TJ Nipples.png":                                      {1: "Titjob/Preg/Rogue TJ NipplesXL.png"},
            "Titjob/Rogue TJ Nipples Piercings.png":                            {1: "Titjob/Preg/Rogue TJ Nipples PiercingsXL.png"},
            "Titjob/Clothes/Chest/Green Bikini Top/Green Bikini Top Down.png":  {1: "Titjob/Preg/Green Bikini Top Down XL.png"},
            "Titjob/Clothes/Chest/Green Bikini Top/Green Bikini Top Handle.png":{1: "Titjob/Preg/Green Bikini Top Handle XL.png"},

            # ---------- Cowgirl (also the masturbation scene) ----------
            # "Torso Preg2" carries the shadow the belly overlay casts: it only makes sense WITH the overlay.
            "Cowgirl/Rogue Cowgirl Torso.png":                                  {1: "Cowgirl/Preg/Rogue Cowgirl Torso Preg.png", 2: "Cowgirl/Preg/Rogue Cowgirl Torso Preg2.png"},
            "+Cowgirl/belly":                                                   {2: "Cowgirl/Preg/Preg Belly.png"},
            "Cowgirl/Rogue Cowgirl Boobs Base.png":                             {1: "Cowgirl/Preg/Rogue Cowgirl Boobs Base XL.png"},
            "Cowgirl/Rogue Cowgirl Nipples.png":                                {1: "Cowgirl/Preg/Rogue Cowgirl Nipples XL.png"},
            "Cowgirl/Rogue Cowgirl Nipples Piercing.png":                       {1: "Cowgirl/Preg/Rogue Cowgirl Nipples Piercings XL.png"},
            "Cowgirl/Clothes/Chest/Top Crop/Rogue Cowgirl Shirt.png":           {1: "Cowgirl/Preg/Rogue Cowgirl Shirt XL.png"},
            "Cowgirl/Clothes/Chest/Green Bikini Top/Green bikini Top Down.png": {1: "Cowgirl/Preg/Green bikini Top Down XL.png"},
            "Cowgirl/Clothes/Chest/Green Bikini Top/Green bikini Top Up.png":   {1: "Cowgirl/Preg/Green bikini Top Up XL.png"},
            # hide-face arm: the mesh shirt it carries covers the breasts
            "Cowgirl/Clothes/Over/Mesh Top/Hide Arm 1 Left Mesh Top.png":       {1: "Cowgirl/Preg/Hide Arm 1 Left Mesh Top Preg.png"},
        },

        "ntw": {
            # ---------- Standing ----------
            "Standing/Negasonic Torso.png":                                     {1: "Standing/Preg/Negasonic TorsoPreg.png"},
            "+Standing/belly":                                                  {2: "Standing/Preg/Negasonic TorsoPreg2.png"},
            "Standing/Negasonic Standing Boobs Naked.png":                      {1: "Standing/Preg/Negasonic Standing Boobs NakedXL.png"},
            "Standing/Negasonic Standing Boobs Naked Piercings.png":            {1: "Standing/Preg/Negasonic Standing Boobs Naked PiercingsXL.png"},
            "Standing/Negasonic Arm Right 4.png":                               {2: "Standing/Preg/Negasonic Arm Right 4Preg.png"},
            "Standing/Clothes/Chest/Yellow Bra/Yellow Bra.png":                 {1: "Standing/Preg/Yellow BraXL.png"},
            "Standing/Clothes/Chest/Yellow Bra/Yellow Bra Up.png":              {1: "Standing/Preg/Yellow Bra UpXL.png"},
            # DownPreg = same top with the lower strings going around the full belly
            "Standing/Clothes/Chest/Pink Bikini Top/Pink Bikini Top Down.png":  {1: "Standing/Preg/Pink Bikini Top DownXL.png", 2: "Standing/Preg/Pink Bikini Top DownPreg.png"},
            "Standing/Clothes/Chest/Pink Bikini Top/Pink Bikini Top Up.png":    {1: "Standing/Preg/Pink Bikini Top UpXL.png"},
            "Standing/Clothes/Negasonic Standing Towel Body.png":               {1: "Standing/Preg/Negasonic Standing Towel BodyXL.png", 2: "Standing/Preg/Copy of Negasonic Standing Towel BodyPreg.png"},
            # Default Uniform. The artist's stage numbers run the OTHER way round from ours: "TorsoXL Stage 2"
            # only has the bigger breasts (visual stage 1), "Default Uniform Stage 1" also wraps the full belly
            # (visual stage 2). Measured: the full belly sticks 560+ px out of the first one, 0 out of the second.
            "Standing/Clothes/Over/Default Uniform/Negasonic Torso Clothed.png": {1: "Standing/Preg/Negasonic TorsoXL Stage 2 Standing.png", 2: "Standing/Preg/Default Uniform Stage 1 Standing.png"},
            "Standing/Clothes/Over/Default Uniform/Negasonic Arm Right 4 Default Uniform.png": {2: "Standing/Preg/Negasonic Arm Right 4 Default UniformPreg.png"},
            # panties cut lower, under the full belly. "Negasonic TorsoPregPreg" IS the worn pink bikini bottom:
            # exported under the wrong name, kept as delivered.
            "Standing/Clothes/Panties/Yellow Panties/Yellow Panties.png":       {2: "Standing/Preg/Yellow PantiesPreg.png"},
            "Standing/Clothes/Panties/Yellow Panties/Yellow Panties Side.png":  {2: "Standing/Preg/Yellow Panties SidePreg.png"},
            "Standing/Clothes/Panties/Pink Bikini Panties/Pink Bikini Bottom Up.png":   {2: "Standing/Preg/Negasonic TorsoPregPreg.png"},
            "Standing/Clothes/Panties/Pink Bikini Panties/Pink Bikini Bottom Side.png": {2: "Standing/Preg/Pink Bikini Bottom SidePreg.png"},

            # ---------- Blowjob (TWO bellies here) ----------
            "Blowjob/Legs.png":                                                 {1: "Blowjob/Preg/LegsPreg.png", 2: "Blowjob/Preg/LegsPreg2.png"},
            # the uniform legs only exist over the full belly
            "Blowjob/Clothes/Over/Default Uniform/BJ Legs Clothed.png":         {2: "Blowjob/Preg/BJ Legs ClothedPreg.png"},
            "Blowjob/Negasonic Chest.png":                                      {1: "Blowjob/Preg/Negasonic ChestXL.png"},
            "Blowjob/Negasonic Chest Piercing.png":                             {1: "Blowjob/Preg/Negasonic Chest PiercingXL.png"},
            # worn tops carry their own skin (the chest body is hidden under them: chest_hidden)
            "Blowjob/Clothes/Chest/Yellow Bra/BJ Boobs Bra.png":                {1: "Blowjob/Preg/BJ Boobs BraXL.png"},
            # the raised bra XL still covers most of the breasts (only the nipple tips show): artist's drawing
            "Blowjob/Clothes/Chest/Yellow Bra/Yellow Bra Up.png":               {1: "Blowjob/Preg/Yellow Bra UpXL.png"},
            "Blowjob/Clothes/Chest/Pink Bikini Top/Pink Bikini Top.png":        {1: "Blowjob/Preg/Pink Bikini TopXL.png"},
            "Blowjob/Clothes/Chest/Pink Bikini Top/Pink Bikini Top Up.png":     {1: "Blowjob/Preg/Pink Bikini Top UpXL.png"},
            "Blowjob/Clothes/Over/Default Uniform/BJ Boobs Clothed.png":        {1: "Blowjob/Preg/BJ Boobs ClothedXL.png"},

            # ---------- Handjob (one belly: stages 1 and 2 look the same) ----------
            "Handjob/Negasonic HJ Body.png":                                    {1: "Handjob/Preg/Negasonic HJ BodyPreg.png"},
            "Handjob/Torso 2.png":                                              {1: "Handjob/Preg/Torso2Preg.png"},
            "Handjob/Negasonic HJ Boobs Naked.png":                             {1: "Handjob/Preg/Negasonic HJ Boobs NakedXL.png"},
            "Handjob/Negasonic HJ Boobs Naked Piercings.png":                   {1: "Handjob/Preg/Negasonic HJ Boobs Naked PiercingsXL.png"},
            "Handjob/Clothes/Chest/Yellow Bra/Yellow Bra.png":                  {1: "Handjob/Preg/Yellow BraXL.png"},
            "Handjob/Clothes/Chest/Yellow Bra/Yellow Bra Up.png":               {1: "Handjob/Preg/Yellow Bra UpXL.png"},
            # the artist also made "TopXL" / "Top UpXL" (bigger breasts, NO belly): unused while the belly is on from stage 1
            "Handjob/Clothes/Chest/Pink Bikini Top/Pink Bikini Top.png":        {1: "Handjob/Preg/Pink Bikini TopPreg.png"},
            "Handjob/Clothes/Chest/Pink Bikini Top/Pink Bikini Top Up.png":     {1: "Handjob/Preg/Copy of Pink Bikini Top UpPreg.png"},
            "Handjob/Clothes/Over/Yellow Jacket/Negasonic HJ Body Clothed.png":   {1: "Handjob/Preg/Negasonic HJ Body ClothedPreg.png"},
            "Handjob/Clothes/Over/Yellow Jacket/Negasonic HJ Body Clothed 2.png": {1: "Handjob/Preg/Negasonic HJ Body Clothed 2Preg.png"},
            "Handjob/Clothes/Over/Yellow Jacket/Negasonic HJ Boobs Clothed.png":  {1: "Handjob/Preg/Negasonic HJ Boobs ClothedXL.png"},

            # ---------- Titjob (one belly, at the bottom edge) ----------
            # Normal art = breasts WITH nipples in one file. XL art = base + separate nipples: both originals
            # turn into the same base and the nipples come as added layers (image ntw titjob_nipples).
            "Titjob/Negasonic TJ Body.png":                                     {1: "Titjob/Preg/Negasonic TJ BodyPreg.png"},
            "Titjob/Negasonic TJ Boobs.png":                                    {1: "Titjob/Preg/Negasonic TJ BoobsBaseXL.png"},
            "Titjob/Negasonic TJ Boobs Piercings.png":                          {1: "Titjob/Preg/Negasonic TJ BoobsBaseXL.png"},
            "+Titjob/nipples":                                                  {1: "Titjob/Preg/Negasonic TJ NipplesXL.png"},
            "+Titjob/nipples pierced":                                          {1: "Titjob/Preg/Negasonic TJ Nipples PiercedXL.png"},

            # ---------- Cowgirl (also the masturbation scene) ----------
            "Cowgirl/Negasonic Cowgirl Torso.png":                              {1: "Cowgirl/Preg/NTW Torso Preg.png"},
            "+Cowgirl/belly":                                                   {2: "Cowgirl/Preg/Belly Preg.png"},
            "Cowgirl/Negasonic Cowgirl Boobs Base.png":                         {1: "Cowgirl/Preg/Negasonic Cowgirl Boobs BaseXL.png"},
            "Cowgirl/Negasonic Cowgirl Nipples.png":                            {1: "Cowgirl/Preg/Negasonic Cowgirl NipplesXL.png"},
            "Cowgirl/Negasonic Cowgirl Nipples Piercings.png":                  {1: "Cowgirl/Preg/Negasonic Cowgirl Nipples PiercingsXL.png"},
            "Cowgirl/Clothes/Chest/Yellow Bra/Yellow Bra.png":                  {1: "Cowgirl/Preg/Yellow BraXL.png"},
            "Cowgirl/Clothes/Chest/Yellow Bra/Yellow Bra Up.png":               {1: "Cowgirl/Preg/Yellow Bra UpXL.png"},
            "Cowgirl/Clothes/Chest/Pink Bikini Top/Pink Bikini Top.png":        {1: "Cowgirl/Preg/Pink Bikini TopXL.png"},
            "Cowgirl/Clothes/Chest/Pink Bikini Top/Pink Bikini Top Up.png":     {1: "Cowgirl/Preg/Pink Bikini Top UpXL.png"},
            "Cowgirl/Clothes/Chest/Pink Bikini Top/Pink Bikini Top Fixed.png":  {1: "Cowgirl/Preg/Pink Bikini Top FixedXL.png"},

            # ---------- Full Nelson ----------
            # The pulled-up tops are drawn from _FN_CHEST_UP_MAPS (Core_FullNelson.rpy), wired there.
            # "+Full Nelson/belly" is ALSO composited on fn_during_pussy_fast: that layer redraws the lower
            # torso above the layeredimage and would cover the belly at fast speed.
            "Full Nelson/Torso.png":                                            {1: "Full Nelson/Preg/TorsoPreg.png"},
            "+Full Nelson/belly":                                               {2: "Full Nelson/Preg/Belly Preg.png"},
            "Full Nelson/Chest.png":                                            {1: "Full Nelson/Preg/ChestPreg.png"},
            "Full Nelson/Nipples.png":                                          {1: "Full Nelson/Preg/NipplesPreg.png"},
            "Full Nelson/Nipples Piercing.png":                                 {1: "Full Nelson/Preg/Nipples PiercingPreg.png"},
            "Full Nelson/Clothes/Yellow Top Down.png":                          {1: "Full Nelson/Preg/Yellow Top DownPreg.png"},
            "Full Nelson/Clothes/Yellow Top Up.png":                            {1: "Full Nelson/Preg/Yellow Top UpPreg.png"},
            "Full Nelson/Clothes/Bikini/Bikini Top Down.png":                   {1: "Full Nelson/Preg/Bikini Top DownPreg.png"},
            "Full Nelson/Clothes/Bikini/Bikini Top Up.png":                     {1: "Full Nelson/Preg/Bikini Top UpPreg.png"},
            "Full Nelson/Cum/Cum Boobs.png":                                    {1: "Full Nelson/Preg/Cum BoobsPreg.png"},
        },

        "tenny": {
            # ---------- Standing ----------
            # The jacket only has an XL version: it hangs open, the belly shows between its sides.
            "Standing/Tenny_Torso.png":                                         {1: "Standing/Preg/Tenny_TorsoPreg1.png"},
            "+Standing/belly":                                                  {2: "Standing/Preg/TennyTorsoPreg2.png"},
            "Standing/Tenny_Chest.png":                                         {1: "Standing/Preg/ChestXL.png"},
            "Standing/Tenny_Chest_Piercing.png":                                {1: "Standing/Preg/ChestPiercingXL.png"},
            "Standing/Tenny Arm Right 4.png":                                   {2: "Standing/Preg/Tenny Arm Right 4Preg.png"},
            # panties and pants cut lower, under the full belly
            "Standing/Clothes/Panties/Striped Panties/Striped Panties.png":     {2: "Standing/Preg/Striped Panties.png"},
            "Standing/Clothes/Panties/Striped Panties/Striped Panties Side.png":{2: "Standing/Preg/Striped Panties Side.png"},
            "Standing/Clothes/Panties/Blue Bikini/Blue Bikini.png":             {2: "Standing/Preg/Blue Bikini.png"},
            "Standing/Clothes/Panties/Blue Bikini/Blue Bikini Side.png":        {2: "Standing/Preg/Blue Bikini Side.png"},
            "Standing/Clothes/Legs/White Legs/Tenny White Legs.png":            {2: "Standing/Preg/Tenny White Legs.png"},
            "Standing/Clothes/Legs/White Legs/Tenny White Legs Wet.png":        {2: "Standing/Preg/Tenny White Legs Wet.png"},
            "Standing/Clothes/Chest/White Bra/White Bra.png":                   {1: "Standing/Preg/White BraXL.png"},
            "Standing/Clothes/Chest/White Bra/White Bra Up.png":                {1: "Standing/Preg/White Bra UpXL.png"},
            "Standing/Clothes/Chest/Blue Bikini Top/Blue Bikini Top.png":       {1: "Standing/Preg/Blue Bikini TopXL.png"},
            "Standing/Clothes/Chest/Blue Bikini Top/Blue Bikini Top Up.png":    {1: "Standing/Preg/Blue Bikini Top UpXL.png"},
            # ShirtPreg = same shirt with the hem riding up over the full belly
            "Standing/Clothes/Mid/Blue Shirt/Tenny Blue Shirt.png":             {1: "Standing/Preg/Tenny Blue ShirtXL.png", 2: "Standing/Preg/Tenny Blue ShirtPreg.png"},
            "Standing/Clothes/Mid/Blue Shirt/Tenny Blue Shirt Up.png":          {1: "Standing/Preg/Tenny Blue Shirt UpXL.png"},
            "Standing/Clothes/Over/Blue Jacket/Tenny Blue Jacket.png":          {1: "Standing/Preg/Tenny Blue JacketXL.png"},
            "Standing/Clothes/Over/Blue Jacket/Tenny Blue Jacket Up.png":       {1: "Standing/Preg/Tenny Blue Jacket UpXL.png"},
            # one towel per arm pose (1 / 2+3 / 4). Their left outline over the bust and the belly is the body's
            # own line: the XL chest and the belly overlay MUST stay drawn under them.
            "Standing/Clothes/Tenny Towel 1.png":                               {1: "Standing/Preg/Tenny Towel 1XL.png", 2: "Standing/Preg/Tenny Towel 1Preg.png"},
            "Standing/Clothes/Tenny Towel 23.png":                              {1: "Standing/Preg/Tenny Towel 23XL.png", 2: "Standing/Preg/Tenny Towel 23Preg.png"},
            "Standing/Clothes/Tenny Towel 4.png":                               {1: "Standing/Preg/Tenny Towel 4XL.png", 2: "Standing/Preg/Tenny Towel 4Preg.png"},

            # ---------- Blowjob + Handjob (same art folder; one belly: stages 1 and 2 look the same) ----------
            # The belly overlay sits right above the torso, below the chest.
            "+BJ_HJ/belly":                                                     {1: "BJ_HJ/Preg/BellyPreg.png"},
            "BJ_HJ/Tenny Chest.png":                                            {1: "BJ_HJ/Preg/ChestXL.png"},
            "BJ_HJ/Tenny Chest Piercing.png":                                   {1: "BJ_HJ/Preg/ChestPiercingsXL.png"},
            "BJ_HJ/Clothes/Chest/Bikini Top/Blue Bikini Top.png":               {1: "BJ_HJ/Preg/Blue Bikini TopXL.png"},
            "BJ_HJ/Clothes/Chest/Top/White Top.png":                            {1: "BJ_HJ/Preg/White TopXL.png"},
            "BJ_HJ/Clothes/Mid/Blue Shirt/Blue Shirt.png":                      {1: "BJ_HJ/Preg/Blue ShirtXL.png"},
            "BJ_HJ/Clothes/Over/Blue Jacket/Blue Jacket.png":                   {1: "BJ_HJ/Preg/Blue JacketXL.png"},

            # ---------- Full Nelson (same notes as NTW's) ----------
            "+Full Nelson/belly":                                               {2: "Full Nelson/Preg/Belly Preg.png"},
            "Full Nelson/Chest.png":                                            {1: "Full Nelson/Preg/ChestXL.png"},
            "Full Nelson/Nipples.png":                                          {1: "Full Nelson/Preg/NipplesXL.png"},
            "Full Nelson/Nipples Piercing.png":                                 {1: "Full Nelson/Preg/Nipples PiercingXL.png"},
            "Full Nelson/Clothes/White Top/White Top Down.png":                 {1: "Full Nelson/Preg/White Top DownXL.png"},
            "Full Nelson/Clothes/White Top/White Top Up.png":                   {1: "Full Nelson/Preg/White Top UpXL.png"},
            "Full Nelson/Clothes/Bikini/Bikini Top Dow.png":                    {1: "Full Nelson/Preg/Bikini Top DownXL.png"},
            "Full Nelson/Clothes/Bikini/Bikini Top Up.png":                     {1: "Full Nelson/Preg/Bikini Top UpPreg.png"},
            # bottoms cut lower, under the full belly
            "Full Nelson/Clothes/Striped Panties/Striped Bottom.png":           {2: "Full Nelson/Preg/Striped BottomPreg.png"},
            "Full Nelson/Clothes/Bikini/Bikini Bottom.png":                     {2: "Full Nelson/Preg/Bikini BottomPreg.png"},
        },

        "shion": {
            # ---------- Standing (stage 1 = the bigger breasts only; the belly and what covers it from stage 2) ----------
            "+Standing/belly":                                                  {2: "Standing/Preg/Belly.png"},
            "Standing/Chest/Chest.png":                                         {1: "Standing/Preg/Chest XL.png"},
            "Standing/Chest/Chest Piercing.png":                                {1: "Standing/Preg/Chest Pierced XL.png"},
            "Standing/Chest/Boobs No Nip.png":                                  {1: "Standing/Preg/Chest XL.png"},
            "Standing/Clothes/Chest Bra/Red Bra.png":                           {1: "Standing/Preg/Red Bra XL.png"},
            "Standing/Clothes/Bikini/Bikini Top.png":                           {1: "Standing/Preg/Bikini Top XL.png"},
            "Standing/Clothes/Chest Bra/Red Bra Down.png":                      {1: "Standing/Preg/Red Bra UP XL.png"},
            "Standing/Clothes/Red Panties/Red Panties.png":                     {2: "Standing/Preg/Panties Preg.png"},
            "Standing/Clothes/Bikini/Bikini Bottom.png":                        {2: "Standing/Preg/Bikini Bottom Preg.png"},
            "Standing/Clothes/Pants Legs/White Pants.png":                      {2: "Standing/Preg/White Pants Preg.png"},
            # The jacket, the vest and the towel are cut around the full belly (stage 2; at stage 1 the normal files
            # over the XL chest). One jacket per arm pose: "Preg 1" (arm 1), "Preg Hand On Hip" (arms 2 and 3, the
            # same normal file), "Preg Crossed" (arm 4, arms crossed: she DOES cross them pregnant, author's call,
            # "preg_crossed_arms" in scene_config). One open vest for every arm pose (the per-arm vest files only
            # differ where the arm overlaps it), from stage 1 (author: the normal vest does not close over the XL
            # chest). Towel from stage 1 (the XL chest needs it).
            "Standing/Clothes/Jacket Over/Jacket Arms 1.png":                   {2: "Standing/Preg/Jacket Preg 1.png"},
            "Standing/Clothes/Jacket Over/Jacket Arms 2.png":                   {2: "Standing/Preg/Jacket Preg Hand On Hip.png"},
            "Standing/Clothes/Jacket Over/Jacket Arms 3.png":                   {2: "Standing/Preg/Jacket Preg Hand On Hip.png"},
            "Standing/Clothes/Jacket Over/Jacket Arms 4.png":                   {2: "Standing/Preg/Jacket Preg Crossed.png"},
            "Standing/Clothes/Vest Mid/Vest Arms 1.png":                        {1: "Standing/Preg/Vest Preg.png"},
            "Standing/Clothes/Vest Mid/Vest Arms 2.png":                        {1: "Standing/Preg/Vest Preg.png"},
            "Standing/Clothes/Vest Mid/Vest Arms 3.png":                        {1: "Standing/Preg/Vest Preg.png"},
            "Standing/Clothes/Vest Mid/Vest Arms 4.png":                        {1: "Standing/Preg/Vest Preg.png"},
            "Standing/Towel/Towell.png":                                        {1: "Standing/Preg/Towell Preg 1.png"},

            # ---------- Blowjob (seen from above) ----------
            # One belly only: stages 1 and 2 look the same here. The legs are redrawn under the belly (the crease).
            "+Blowjob/preg":                                                    {1: "Blowjob/Preg/Preg.png"},
            "Blowjob/Legs.png":                                                 {1: "Blowjob/Preg/Legs.png"},
            "Blowjob/Chest/Chest.png":                                          {1: "Blowjob/Preg/Chest XL.png"},
            "Blowjob/Chest/Chest Piercing.png":                                 {1: "Blowjob/Preg/Chest Pierced XL.png"},
            "Blowjob/Clothes/Bikini Top.png":                                   {1: "Blowjob/Preg/Bikini XL.png"},
            "Blowjob/Clothes/Bra.png":                                          {1: "Blowjob/Preg/Bra XL.png"},

            # ---------- Handjob (the belly only shows at the bottom edge of the frame) ----------
            "+Handjob/belly":                                                   {1: "Handjob/Preg/Belly.png"},
            "Handjob/Chest/Chest.png":                                          {1: "Handjob/Preg/Chest XL.png"},
            "Handjob/Chest/Chest Piercing.png":                                 {1: "Handjob/Preg/Chest Pierced XL.png"},
            "Handjob/Clothes/Bikini.png":                                       {1: "Handjob/Preg/Bikini XL.png"},
            "Handjob/Clothes/Bra.png":                                          {1: "Handjob/Preg/Bra XL.png"},

            # ---------- Titjob (the belly shows at the bottom edge; one belly) ----------
            # Her titjob is done in a bra / bikini top or bare (author's rule, 2026-10-05): the "Jacket Arms N XL"
            # and "Vest XL" files stay in Titjob/Preg unwired. No XL bra / bikini top yet (shion tj_bra /
            # tj_bikini_top, above the boobs): the normal cups.
            "Titjob/Torso.png":                                                 {1: "Titjob/Preg/Torso Preg.png"},
            "Titjob/Chest/Chest.png":                                           {1: "Titjob/Preg/Chest XL.png"},
            "Titjob/Chest/Nipples.png":                                         {1: "Titjob/Preg/Nipples XL.png"},
            "Titjob/Chest/Nipples Piercing.png":                                {1: "Titjob/Preg/Nipples Pierced XL.png"},

            # ---------- Rimjob (her own layers, Images/Shion/Rimjob.rpy; one belly, hanging under the torso) ----------
            # The belly is an added layer above the far arm and under the chest (rj_belly, z 9963); the open vest and
            # the XL bra / bikini top sit over it. No XL jacket: the jacket only covers her back and arms there.
            "+Rimjob/belly":                                                    {1: "Rimjob/Preg/Belly Preg.png"},
            "Rimjob/Chest/Chest.png":                                           {1: "Rimjob/Preg/Chest XL.png"},
            "Rimjob/Chest/Chest No Niples.png":                                 {1: "Rimjob/Preg/Chest No Niples.png"},
            "Rimjob/Chest/Chest Piercing.png":                                  {1: "Rimjob/Preg/Chest Pierced XL.png"},
            "Rimjob/Clothes/Bra.png":                                           {1: "Rimjob/Preg/Bra XL.png"},
            "Rimjob/Clothes/Bikini Top.png":                                    {1: "Rimjob/Preg/Bikini Top XL.png"},
            "Rimjob/Clothes/Vest.png":                                          {1: "Rimjob/Preg/Vest Preg.png"},

            # ---------- Cowgirl (her own layers, Images/Shion/Cowgirl.rpy) ----------
            # The XL chest has the nipples drawn in: the nipples layer goes away (None), the pierced XL chest
            # replaces the pierced nipples layer (drawn over the plain XL chest). No XL bra yet: the normal one.
            "+Cowgirl/belly":                                                   {1: "Cowgirl/Preg/Belly.png"},
            "Cowgirl/Chest/Chest.png":                                          {1: "Cowgirl/Preg/Chest XL.png"},
            "Cowgirl/Chest/Nipples.png":                                        {1: None},
            "Cowgirl/Chest/Nipples Piercing.png":                               {1: "Cowgirl/Preg/Chest Pierced XL.png"},
            "Cowgirl/Clothes/Bikini Top.png":                                   {1: "Cowgirl/Preg/Bikini XL.png"},
        },
    }

    # Console preview, {gid: stage}. Init-time dict, only ever MUTATED in place: Ren'Py saves a store
    # variable when it is rebound after init, so a preview never reaches a save file.
    _PREG_ART_PREVIEW = {}

    # Zoom applied to pregnancy VARIANT images: when an artist delivers preg art at a different
    # resolution from the base sprite, list the gid here with the scale factor (0.5 = half size), or
    # {key: factor} where a key is a pose folder ("Standing") or ONE variant file (relative to her
    # folder; a file beats its folder). Shion's first Standing batch came at 2x (960 x 1920, listed
    # file by file); the later Standing files (jacket, vest, towel) came at the sprite's size.
    # An ORIGINAL is never zoomed: it must come at the sprite's size (a 2x original doubles the whole
    # layered image and the sprite slides off the screen); _preg_art_validate() warns about it.
    _PREG_ART_SCALE = {
        "shion": {
            # "Jacket Preg 1" and "Red Bra XL" were re-exported at the sprite's size (480x960, measured
            # 2026-10-11): their 0.5 stayed behind and drew a HALF-SIZE bra floating by her head
            # (tester's screenshot). The other Standing files are still the 2x batch.
            "Standing/Preg/Belly.png":              0.5,
            "Standing/Preg/Chest XL.png":           0.5,
            "Standing/Preg/Chest Pierced XL.png":   0.5,
            "Standing/Preg/Red Bra UP XL.png":      0.5,
            "Standing/Preg/Bikini Top XL.png":      0.5,
            "Standing/Preg/Panties Preg.png":       0.5,
            "Standing/Preg/Bikini Bottom Preg.png": 0.5,
            "Standing/Preg/White Pants Preg.png":   0.5,
        },
    }

    def _preg_art_scale(gid, variant):
        """The zoom of one variant file (relative to her folder), or None."""
        _s = _PREG_ART_SCALE.get(gid)
        if isinstance(_s, dict):
            return _s.get(variant, _s.get(variant.split("/")[0]))
        return _s

    # Every (gid, original) a character file asked for, for _preg_art_validate()
    _PREG_ART_WIRED = set()

    def preg_vstage(gid):
        """Visual pregnancy stage of the girl with this gid (0 when she does not exist)."""
        _girl = GIRL_BY_ID.get(gid)
        return pregnancy_visual_stage(_girl) if _girl else 0

    def preg_art(gid, original):
        """Displayable of ONE art layer of girl `gid`: the original file, or the variant PREG_ART lists
        for her current visual pregnancy stage. `original` is relative to images/characters/<Girl>/; a
        "+" key is an added layer (Null below its first stage). Same shape as _p() for the player skin."""
        _root = "images/characters/%s/" % _GIRL_ASSET_FOLDER[gid]
        _normal = Null() if original.startswith("+") else _root + original
        _variants = PREG_ART.get(gid, {}).get(original)
        _PREG_ART_WIRED.add((gid, original))
        if not _variants:
            print("[PREG_ART] WARNING %s: '%s' is wired in an image but has no PREG_ART entry (always the original)" % (gid, original))
            return _normal
        _args = []
        for _stage in sorted(_variants, reverse=True):
            if _variants[_stage] is None:
                _args += ["preg_vstage('%s') >= %d" % (gid, _stage), Null()]
                continue
            _disp = _root + _variants[_stage]
            _scale = _preg_art_scale(gid, _variants[_stage])
            if _scale:
                _disp = Transform(_disp, zoom=_scale)
            _args += ["preg_vstage('%s') >= %d" % (gid, _stage), _disp]
        _args += ["True", _normal]
        return ConditionSwitch(*_args)

    # ------------------------------------------------------------------ belly motion (riding scenes)
    # The full-belly overlay of the Cowgirl and the Full Nelson moves a little on its own, on top of the body's
    # bounce: it follows the body's LIVE yoffset (whatever drives it: the Cowgirl clock function, the Full Nelson
    # ATL, an impact...), a touch late and a touch further, so it reads as weight and not as a sticker. With the
    # body at rest it sits exactly where it was drawn.
    #   gain    how much further than the body it travels (x the body's distance from the middle of its swing)
    #   lag     seconds it trails the body (the same at every speed)
    #   window  seconds of body motion the "middle of the swing" is taken from (longer than the slowest cycle, 2.0 s)
    #   settle  seconds the middle takes to glide to a new place (speed change, stop): no pop when old motion leaves the window
    #   limit   px it may ever drift from where it was drawn, approached softly (its outline meets the torso's:
    #           measured on the art, up to 8 px still reads as one body)
    PREG_BELLY_MOTION = {"gain": 0.07, "lag": 0.05, "window": 2.5, "settle": 0.4, "limit": 6.0}

    # {gid: filter state}. Init-time dict mutated in place: visual only, never saved.
    _PREG_BELLY_STATE = {}

    def _preg_belly_body_y(gid, body_tag=None):
        """Live yoffset of her body image (tag = gid on master, or `body_tag` for a girl whose riding layers carry
        their own tags: Shion's scg_torso_bottom): the sum over her at_list. None when she is not shown."""
        try:
            _d = renpy.game.context().scene_lists.get_displayable_by_tag("master", body_tag or gid)
        except Exception:
            return None
        _y = None
        while isinstance(_d, renpy.display.transform.Transform):
            _y = (_y or 0.0) + float(_d.yoffset or 0.0)
            _d = _d.child
        return _y

    def _preg_belly_extra(gid, body_tag=None):
        """Px the belly overlay sits below (+) / above (-) its drawn place right now. ONE value per frame per girl:
        the copy inside the layeredimage and the one riding on the Full Nelson fast layer must agree."""
        import time, math
        _now = time.time()
        _s = _PREG_BELLY_STATE.setdefault(gid, {"t": 0.0, "hist": [], "center": 0.0, "extra": 0.0, "moving": False, "log": 0.0})
        _dt = _now - _s["t"]
        if _dt < 0.008:                                     # same frame: the other copy already asked
            return _s["extra"]
        _y = _preg_belly_body_y(gid, body_tag)
        _s["t"] = _now
        if _y is None or not _s["hist"] or _dt > 0.5:       # not shown / first frame / back after a pause: start at rest
            _s.update(hist=[(_now, _y)] if _y is not None else [], center=_y or 0.0, extra=0.0, moving=False)
            return 0.0
        _m = PREG_BELLY_MOTION
        _hist = _s["hist"]
        _hist.append((_now, _y))
        while _hist[0][0] < _now - _m["window"]:
            _hist.pop(0)
        _lo = min(_h[1] for _h in _hist)
        _hi = max(_h[1] for _h in _hist)
        _s["center"] += ((_lo + _hi) / 2.0 - _s["center"]) * (1.0 - math.exp(-_dt / _m["settle"]))
        # where the body was `lag` seconds ago (between the two samples around that moment)
        _then = _now - _m["lag"]
        _i = len(_hist) - 1
        while _i > 0 and _hist[_i][0] > _then:
            _i -= 1
        _t0, _y0 = _hist[_i]
        _t1, _y1 = _hist[min(_i + 1, len(_hist) - 1)]
        _yd = _y0 if _t1 <= _t0 or _then <= _t0 else _y0 + (_y1 - _y0) * (_then - _t0) / (_t1 - _t0)
        _s["extra"] = _m["limit"] * math.tanh(_m["gain"] * (_yd - _s["center"]) / _m["limit"])
        _s["moving"] = (_hi - _lo) > 0.05 or abs(_s["extra"]) > 0.02
        if _s["moving"] and _now - _s["log"] > 3.0:
            _s["log"] = _now
            print("[PREG_BELLY] %s body_y=%.1f swing=%.1f..%.1f belly_extra=%+.2f px (gain=%s lag=%s limit=%s)" % (gid, _y, _lo, _hi, _s["extra"], _m["gain"], _m["lag"], _m["limit"]))
        return _s["extra"]

    def _preg_belly_motion(gid, window_top, body_tag, first_stage, trans, st, at):
        """Transform function of a riding-scene belly overlay."""
        if preg_vstage(gid) < first_stage:                  # no belly on screen: nothing to move, look again later
            return 0.5
        _extra = _preg_belly_extra(gid, body_tag)
        if window_top is None:
            trans.yoffset = _extra
        else:
            # the copy riding on a layer drawn ABOVE the body: the window stays put, the belly slides inside it
            _e = int(round(_extra))
            trans.crop = (0, window_top - _e, 1920, 1080 - window_top + _e)
        return 0 if _PREG_BELLY_STATE[gid]["moving"] else 0.1

    def preg_belly(gid, key, window_top=None, body_tag=None):
        """preg_art() for the belly overlay `key` of a scene where she rides, with its own small motion (from the
        first stage the key lists: 2 for the full belly of most girls, 1 for Shion's one belly).
        window_top: for the copy that rides ON a layer drawn above the body (Full Nelson fast layer, placed at
        (0, window_top) of a 1920 x 1080 Composite): only the rows from window_top down show.
        body_tag: the tag of the body layer to follow when it is not her gid (Shion's own cowgirl layers)."""
        _first = min(PREG_ART.get(gid, {}).get(key) or {2: None})
        return Transform(preg_art(gid, key), function=renpy.partial(_preg_belly_motion, gid, window_top, body_tag, _first), subpixel=True)

    def preg_art_preview(girl=None, stage=None):
        """Console: preg_art_preview(Gwen, 2) shows her art at that visual stage right now, whatever
        her real state and the pregnancy mode. preg_art_preview(Gwen) goes back to the real state,
        preg_art_preview() clears every preview."""
        if girl is None:
            _PREG_ART_PREVIEW.clear()
        elif stage is None:
            _PREG_ART_PREVIEW.pop(girl.gid, None)
        else:
            _PREG_ART_PREVIEW[girl.gid] = max(0, min(2, int(stage)))
        print("[PREG_ART] preview = %s" % dict(_PREG_ART_PREVIEW))
        renpy.restart_interaction()
        return "preview: %s" % (dict(_PREG_ART_PREVIEW) or "off, real state")

init 999 python:

    def _preg_art_png_size(path):
        """(width, height) of a PNG read from its header, without decoding the image; None when unreadable."""
        import struct
        try:
            _fh = renpy.open_file(path, encoding=False)     # binary whatever config.open_file_encoding says
            try:
                _head = _fh.read(24)
            finally:
                _fh.close()
        except Exception:
            return None
        if len(_head) < 24 or _head[:8] != b"\x89PNG\r\n\x1a\n":
            return None
        return struct.unpack(">II", _head[16:24])

    def _preg_art_validate():
        """Every file of PREG_ART exists, and every entry is wired in an image (a typo in a key, or a
        forgotten preg_art() call, would silently keep the normal art). Every variant shows at the size
        of its original (its _PREG_ART_SCALE zoom applied): a layer of another size resizes the whole
        layered image and the sprite slides away (Shion's 2x "Jacket Arms 1" took her off the screen)."""
        _bad = 0
        for _gid, _pairs in PREG_ART.items():
            _root = "images/characters/%s/" % _GIRL_ASSET_FOLDER[_gid]
            for _original, _variants in _pairs.items():
                _files = [_v for _v in _variants.values() if _v] + ([] if _original.startswith("+") else [_original])
                for _f in _files:
                    if not renpy.loadable(_root + _f):
                        print("[PREG_ART] WARNING %s: file not found: %s" % (_gid, _root + _f))
                        _bad += 1
                if (_gid, _original) not in _PREG_ART_WIRED:
                    print("[PREG_ART] WARNING %s: '%s' is in PREG_ART but no image uses preg_art() for it" % (_gid, _original))
                    _bad += 1
                # an added "+" layer has no original to compare with; a missing file is reported above
                _osize = None if _original.startswith("+") else _preg_art_png_size(_root + _original)
                if not _osize:
                    continue
                for _stage, _v in sorted(_variants.items()):
                    _vsize = _preg_art_png_size(_root + _v) if _v else None
                    if not _vsize:
                        continue
                    _z = _preg_art_scale(_gid, _v) or 1
                    _shown = (int(round(_vsize[0] * _z)), int(round(_vsize[1] * _z)))
                    if _shown != tuple(_osize):
                        print("[PREG_ART] WARNING %s: '%s' is %dx%d but its stage %d variant '%s' shows at %dx%d (file %dx%d, zoom %s): one of the two came at another size" % (
                            _gid, _original, _osize[0], _osize[1], _stage, _v, _shown[0], _shown[1], _vsize[0], _vsize[1], _z))
                        _bad += 1
        print("[PREG_ART] %d layer(s) registered for %s, %d problem(s)" % (
            sum(len(_p) for _p in PREG_ART.values()), ", ".join(sorted(PREG_ART)), _bad))

    _preg_art_validate()
