Les classes possibles:
    1. Game
        Attributes:
            name
            players
            map
            game_time
        Methods:
            start_game()
            pause_game()
            end_game()
    
    2. Map
        Attributes:
            size:120x120
            terrain_nature (soil, water: ~)
            resource (wood, food, gold)
            players_position
        Methods:
            generate_map(): aleatoirement (il faut expliquer pourquoi).
            resources_position()
            
        commentaire: deux types différents de carte chacune avec des stratégies:
                une avec des ressources réparties sur la carte (carte Arabia d'AoE2)
                une où tout l'or est au centre de la carte
    
    3. Population:
        Attributs:
            number: constant=200
            name (de la population)
            unit
            ...
    
    4. Unit
        Attributes:
            letter
            name
            health (le truc en hp)
            attack
            speed
            cost
            training_time
            range
        Methods:
            move()
            attack()
            training()
            die()

        commentaire: pensez à regarder les units pour connaitre 
        les lettres, noms, cost... (pages 367,368)
    
    5. Resource:
        Attributes:
            type (wood, food, gold)
            quantity
        Methods:
            collect()
        
        commentaire: page 367 pour des infos sur les ressources
    
    6. Building:
        Attributes:
            letter
            name
            health (le truc en hp)
            cost
            build_time
            units_spawn
            population
            Drop_point
            size
        Methods:
            spawn_unit()
            damage()
            Drop_ressource()
            population_increase();
            repair()

        commentaire: page 368-369 pour des infos
    
    7. Menu:
        Attrubutes:
            population
            game
            file
        Methods:
            new_game()
            save()
            load()
            exit()
            pause()
            resume()

    8. Strategy:
        Attributes:
            type (agressive, defensive, balanced)
            tactics
        Methods:
            strategy_choose()
        
    9. Starting_cond:
        Attributs:
            type
            building
            unit
            population
            resource
        
        commentaire: page 369 pour des infos
    
    10. AI (Artificial Intelligence)
            Attributes:
                strategy
            Methods:
                choose_strategy()
                control_units()
                manage_resources()

    11. Combat:
        Attributes:
            attack_units
            defend_units
            terrain_bonus
            result
        Methods:
            damage()
            resolve_battle()
    
    12.Resource_gather
        Attributes:
            resource
            capacity
        Methods:
            gather()
        
    13.Player
        Attributes:
            player_id
            name
            population
            resource
            unit
            building
        Methods:
            gather_resources()
            build_structure()
            train_unit()
            attack()