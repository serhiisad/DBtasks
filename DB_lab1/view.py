
from entities.entities import *
import randomize_db
from datetime import *
from database import Database
import pandas

db = Database()

# data input methods
def input_developer():
   params = input("type <fullname, birth-date, married(1,0)>:").split(",")
   return Developer(*params)

def input_teamlead():
   fullname = input("type <fullname>:")
   return Teamlead(fullname)

def input_team():
   name = input("type <team_name>:")
   return Team(name)

def input_project():
   params = input("type <title, type>:").split(",")
   return Project(*params)

def input_teamid_and_projectid():
   params = input("type <team_id, project_id>:").split(" ")
   return {"team_id": params[0], "project_id": params[1]}

#for search in range
def input_dates_range():
   # dates = input("enter dates to search between: ").split(" ")
   date1 = input("enter date1(in quotes): ")
   date2 = input("enter date2: ")
   return [date1, str(date2)]
   # if date.strftime(date1, "yyyy-mm-dd") > date.strftime(date2, "yyyy-mm-dd"):
   #    raise Exception("incorrect range")

#for full text search
def input_fulltextsearch_data():
   table_name = input("Enter table_name: ")
   field_names_list = input("Enter fields to search among: ").replace(" ", "").split(",")
   #myList = ','.join(map(str, myList))
   field_names_str = ",".join(field_names_list)
   query = input("Enter query:<using <->, |, &, ! etc>: ")
   return [table_name, field_names_str, query]

#for UI
entities_d = {
   1: "Developer",
   2: "Team",
   3: "Project",
   4: "Teamlead",
   5: "Team_Project"
}

tables_to_get_d = {
   1: "Developers, teams, teamleads",
   2: "teams and their projects",
   3: "teams",
   4: "developers",
   5: "teamleads",
   6: "projects"
}

search_methods_d = {
   1: "search for developers by birth in range",
   2: "search for married developers"
}


def create():
   while True:
      print("-----Create-----")
      print_menu(entities_d)
      #try:
      command = input("choose entity:")
      #except ValueError: pass
      if command == 'q': break
      elif int(command) == 1:
         db.create_developer(input_developer())
         break
      elif int(command) == 2:
         db.create_team(input_team())
         break
      elif int(command) == 3:
         db.create_project(input_project())
         break
      elif int(command) == 4:
         db.create_teamlead(input_teamlead())
         break
      elif int(command) == 5:
         db.add_project_for_team(input_teamid_and_projectid())
         break
      else: pass


def update():
   while True:
      print("-----Update-----")
      print_menu(entities_d, maxlen=4)
      command = input("choose entity:")
      _id = input("enter id: ")
      if command == 'q': break
      else:
         if int(command) == 1:
            db.update_developer(_id, input_developer())
            break
         elif int(command) == 2:
            db.update_team(_id, input_team())
            break
         elif int(command) == 3:
            db.update_project(_id, input_project())
            break
         elif int(command) == 4:
            db.update_teamlead(_id, input_teamlead())
            break
         else: pass

def delete():
   while True:
      print("-----Delete-----")
      print_menu(entities_d, maxlen=4)
      command = input("choose entity:")
      entity_id = int(input("enter id: "))
      if command == 'q': break
      elif int(command) == 1:
         db.delete_developer(entity_id)
         break
      elif int(command) == 2:
         db.delete_team(entity_id)
         break
      elif int(command) == 3:
         db.delete_project(entity_id)
         break
      elif int(command) == 4:
         db.delete_teamlead(entity_id)
         break
      else: pass

#fine
def get():
   while True:
      try:
         print("-----Get------")
         print_menu(tables_to_get_d)
         command = int(input("Choose a table to print: "))
      except ValueError: pass
      if command == 1:
         # print(pandas.read_sql(db.get_devs_teams_teamleads(), db.connection))
         print(db.table_toString(db.get_devs_teams_teamleads()))
         break
      elif command == 2:
         print(db.table_toString(db.get_teams_projects()))
         break
      elif command == 3:
         print(db.table_toString(db.get_teams()))
         break
      elif command == 4:
         print(db.table_toString(db.get_developers()))
         break
      elif command == 5:
         print(db.table_toString(db.get_teamleads()))
         break
      elif command == 6:
         print(db.table_toString(db.get_projects()))
         break
      elif str(command) == 'q': break
      else:  pass


def search():
   while True:
      try:
         print("-----Get------")
         print_menu(search_methods_d)
         command = int(input("Choose search method: "))
      except ValueError: pass
      if command == 1:
         dates = input_dates_range()
         print(db.table_toString(db.search_for_devs_birth_in_range(dates[0], dates[1])))
         break
      elif command == 2:
         ismarried = input("input <True/False>: ")
         if(ismarried == "true"): ismarried = True
         else: ismarried = False
         #print(str(ismarried))
         print(db.table_toString(db.search_for_married_devs(ismarried)))
         break
      else: pass


def fulltext_search():
   try:
      print("-----full text search------")
      search_data = input_fulltextsearch_data()
   except ValueError: pass
   print(db.fulltextsearch_by_query(*search_data))
   print(db.table_toString(db.fulltextsearch_by_query(*search_data)))



def random_fill():
   params = input("type<how many projects, teamleads, teams, devs> in DB:").split(",")
   num_params = list(int(par) for par in params)
   randomize_db.random_fill_db(*num_params)

commands_d = {
   1: create,
   2: update,
   3: delete,
   4: get,
   5: search,
   6: fulltext_search,
   7: random_fill
}

def print_menu(menu_dict, maxlen=None):
   print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>")
   if maxlen is None:
      maxlen = len(menu_dict.items())
   if isinstance(list(menu_dict.values())[0], str):
      for key, value in list(menu_dict.items())[0:maxlen]:
         print(key, value)
   else:
      for key, value in list(menu_dict.items())[0:maxlen]:
         print(key, value.__name__)
   print("<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")


def listen():
   while True:
      print_menu(commands_d)
      command = input("Enter command: ")
      if not command.isdigit():
         if command == 'q':
            print("END")
            break
         elif command == 'h':
            print_menu(commands_d)
         else: pass
      elif int(command) in commands_d:
         try:
            commands_d[int(command)]()
         except: print("incorrect input")
      else: pass










