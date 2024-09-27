# 6CCS3PRJ-
**Playing with Complexity: An Interactive
Approach to NP-Hardness in Pac-Man**

**Abstract**

This dissertation explores the iconic arcade game Pac-Man and discusses how it can be
proved to be an NP-hard problem within the realm of complexity theory. By analysing the
details and intricacies of the game mechanics and utilising existing proofs, the project not only
establishes a method of creating Pac-Man levels with just a simple Boolean Formula input
but also introduces a practical method for generating playable levels based on NP-Hardness
proofs. This allows the theoretical work to be translated into an interactive game experience,
thereby enhancing the educational value of complexity theory through gamification and visual
representation. The software developed as part of this dissertation allows users to dynamically
create and play levels derived from NP-hard reductions, offering a useful tool for understanding
and visualizing complex computational concepts. This work can also be built upon for future
work, perhaps with other classic arcade games.

The program allows a user to create a Pac-Man level by just inputting a logic formula
represented by clauses in Conjunctive-Normal-Form (CNF). This is then converted into a graph
for the level conversion. The user has control over other aspects of the level as well, such as
ghost count and level name. Once a user has created a level, it is saved into a database, which
can be viewed and interacted with by the user. The user is able to select a level in the database
and view attributes about this level, such as name and high score. They can also delete the
level if they want to. Levels saved in the database are playable by the user. Playing a level
involves the opening of the Pac-Man GUI, which temporally puts the main GUI on freeze.
The program has two main sections. The first section contains the main GUI and the logic
behind translating and implementing the Pac-Man map, and the second section houses the
Pac-Man game engine. The first section is what is new here, as the Pac-Man game engine just
needs to be able to simulate a Pac-Man game, which is trivial since there are already many
modules and packages to solve this problem.
