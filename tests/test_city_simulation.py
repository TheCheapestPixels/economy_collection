from economy_collection import simple_city_economy as SCE
from economy_collection import economy
from economy_collection import crafting

import unittest


class TestMyCity(unittest.TestCase):
    """I'm assuming the economy functions work."""
    def setUp(self):
        self.E = SCE.Econ() # probably a cyber system.
        
        my_list = [ SCE.city((0,0),
                population = 10,
                resources = {},
                special_jobs = {"administration":4,"traders":2,"craftsmen":2,"politician":2},
                inventory = {"money":{"amount":10},"Food":{"amount":10},"Consumer Goods":{"amount":10},},
                ),
		
        SCE.city((1,1), 
            population = 4,
            resources = {"farming":{"available":4,"occupied":4,"produces":"Wheat"}},
            inventory = {"Food":{"amount":4},"Consumer Goods":{"amount":4},"money":{"amount":5}},
            ),
            
        SCE.city((3,1), 
            population = 4,
            resources = {"farming":{"available":5,"occupied":4,"produces":"Wheat"}},
            inventory = {"Food":{"amount":4},"Consumer Goods":{"amount":4},"money":{"amount":5}},
            ),
		
        SCE.city((-1,3),
            population = 4,
            resources = {"harvesting":{"available":5,"occupied":4,"produces":"Wood"}},
            inventory = {"Food":{"amount":4},"Consumer Goods":{"amount":4},"money":{"amount":5}},
            ),
		
        SCE.city((1,5),
            population = 1,
            resources = {"mining":{"available":5,"occupied":1,"produces":"Iron"}},
            inventory = {"Food":{"amount":1},"Consumer Goods":{"amount":1},"money":{"amount":5}},
            ),
        ]
        
        for x in my_list:
            self.E.cyber_econ.elements.append(x.cyber)
    
    def tearDown(self):
        self.E = None
        
    def test_basics(self):
        
        self.E.main()
        
        # just go one tick?
    
    def test_trading_production(self):
        
        # let's see.
        # I can plan production.
        # not entirely sure how to do time planning.
        
        # craft production is free ish? one craftsman does 1000 things per tick? something like that?
        
        # I should really rather translate individual schedules to statistical man hours.
        
        # so, from schedule_funcs, I'm getting some mix of working hours.
        # I'm "spending" that on certain activities.
        
        my_list = self.E.cyber_econ.elements
        # these will sell some stuff, buy some stuff.
        my_list[0].payload.inventory = {"Food":{"amount":23},"Consumer Goods":{"amount":0},"money":{"amount":100}}
        my_list[1].payload.inventory = {"Food":{"amount":0},"Consumer Goods":{"amount":23},"money":{"amount":100},"Wheat":{"amount":2},"Water":{"amount":2}}
        
        # these will just buy
        my_list[2].payload.inventory = {"Food":{"amount":0},"Consumer Goods":{"amount":0},"money":{"amount":100}}
        my_list[3].payload.inventory = {"Food":{"amount":0},"Consumer Goods":{"amount":0},"money":{"amount":100}}
        my_list[4].payload.inventory = {"Food":{"amount":0},"Consumer Goods":{"amount":0},"money":{"amount":100}}
        
        materials, products, recipes = crafting.default()
        
        my_list[0].payload.recipes["Bread"] = recipes["Bread"]
        my_list[1].payload.recipes["Bread"] = recipes["Bread"]
        
        
        econ_env = economy.EconomyEnvironment()
        M = economy.Market()
        
        for my_object in my_list:
            trader = my_object.payload.econ_agent
            trader.inventory =  my_object.payload.inventory
            M.set_up_trader(trader)
        
        econ_env.locations[M.id] = M
             
        # I need to set up the environment the market,
        # the offers, etc. before I do my production planning.
        
        for cyberob in my_list:
            cyberob.payload.consumption_planning()
            cyberob.payload.selling_planning_tick()
            cyberob.payload.production_planning(econ_env)
            cyberob.payload.market_interaction_planning()
        
    def test_basic_currency_flow_stocks_based_trade(self):
        """same setup as the basics. Maybe I should do this as a 
        setup, teardown, thing."""
        
        # so in this test, I want some very basic needs, exchange.
        
        # independently of production,
        # I can do the trading already.
        # if the setup is right. so.
        
        
        my_list = self.E.cyber_econ.elements
        
        # these will sell some stuff, buy some stuff.
        my_list[0].payload.inventory = {"Food":{"amount":23},"Consumer Goods":{"amount":0},"money":{"amount":100}}
        my_list[1].payload.inventory = {"Food":{"amount":0},"Consumer Goods":{"amount":23},"money":{"amount":100}}
        
        # these will just buy
        my_list[2].payload.inventory = {"Food":{"amount":0},"Consumer Goods":{"amount":0},"money":{"amount":100}}
        my_list[3].payload.inventory = {"Food":{"amount":0},"Consumer Goods":{"amount":0},"money":{"amount":100}}
        my_list[4].payload.inventory = {"Food":{"amount":0},"Consumer Goods":{"amount":0},"money":{"amount":100}}
        
        
        for city in my_list:
            city.payload.econ_agent.inventory = city.payload.inventory
        
        # this is testing the simply_city_economy_main
        # in steps:
        
        for x in my_list:
            x.payload.planning_step(1)
        
        # this should set up offered goods:
        
        assert my_list[0].payload.econ_agent.offered_goods == {'Food': {'amount': 13}}
        assert my_list[1].payload.econ_agent.offered_goods == {'Consumer Goods': {'amount': 19}}

        # set up selling and buying the same way.
        # possibly automate this.
        my_city_list=[]
        for x in my_list:
            my_city_list.append(x.payload)
        
        for x in my_list:
            x.payload.execution_step(1,environment = my_city_list)
        
        for x in my_city_list:
            assert x.inventory["Food"]["amount"] == 0
            assert x.inventory["Consumer Goods"]["amount"] == 0
        
        
        
        l = [{'Consumer Goods': 10, 'money': 3, 'Food': -13},
            {'Consumer Goods': -19, 'money': 15, 'Food': 4},
            {'Food': 4, 'money': -8, 'Consumer Goods': 4},
            {'Food': 4, 'money': -8, 'Consumer Goods': 4},
            {'Food': 1, 'money': -2, 'Consumer Goods': 1},
            ]


        results = []
        for x in my_list:
            results.append(x.payload.econ_agent.sum_difference_from_transactions())
        
        m = len(results)
        c = 0
        while c < m:
            data = l[c]
            result =  results[c]
            assert data == result
            c += 1
        
        
        # render_my_cities(self.E)
        
            
def render_my_cities(environment):
    
    from geom import geom
    from vector import vector
    
    texts = []
    
    geoml = []
    for x in environment.cyber_econ.elements:
        city = x.payload
        position = vector.Vector(* city.pos,0)
        
        circle = geom.circle(local_position = position,radius = 0.1)
        geoml.append(circle)
        
        diffs = city.econ_agent.sum_difference_from_transactions()
        
        y = vector.Vector(0,0.2,0)
        c =0
        for x in city.inventory:
            if x in diffs:
                text = geom.Text(local_position = position + vector.Vector(0.3,0.3,0)+c*y,text = f"{x}:{city.inventory[x]['amount']}, diff {diffs[x]}")
            else:
                text = geom.Text(local_position = position + vector.Vector(0.3,0.3,0)+c*y,text = f"{x}:{city.inventory[x]['amount']}")
            text.style = "text-anchor:start;"
            texts.append(text)
            c += 1

        text = geom.Text(local_position = position + vector.Vector(0.3,0.3,0)+c*y,text = f"population:{city.population}")
        text.style = "text-anchor:start;"
        texts.append(text)
        
        
        
    done = []
    for x in environment.cyber_econ.elements:
        city = x.payload
        for x2 in environment.cyber_econ.elements:
            city2 = x2.payload
            
            if x == x2:
                continue
            
            id_tuple = []
            id_tuple.sort()
            if id_tuple in done:
                continue
                
            done.append((city.id,city2.id))
            
            p1 = vector.Vector(*city.pos,0)
            p2 = vector.Vector(*city2.pos,0)
            
            line = geom.Line.from_two_points(p1,p2)
            geoml.append(line)
    
    bb = geom.calculate_bounding_box(geoml)
    values, points = bb
    rx = values[1] - values[0]
    ry = values[3] - values[2]
    
    my_rect= geom.rectangle(local_position =vector.Vector(values[0]-rx/2,values[2]-ry/2,0),d_vec = vector.Vector(rx*2,ry*2,0))
    my_rect.style = "fill:white;"
    
    geoml = [my_rect] + geoml
            
    fl = []
    
    geoml+=texts
    
    for x in geoml:
        fl.append(x.as_svg())
    
    view_box_d = geom.make_view_box_d(geoml)
    
    geom.main_svg(fl,"city_render_test.svg",view_box_d=view_box_d)

def single_test():
    
    my_object = TestMyCity()
    my_object.setUp()
    my_object.test_trading_production()
    my_object.tearDown()
    
if __name__=="__main__":
    # unittest.main()
    single_test()
