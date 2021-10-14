class Task:
  # конструктор для объекта класса Task ("Задача")
  def __init__(self, id, act_db : dict, start_date = None, finish_date = None, duration = None, not_early_date = None):
    self.id = id                         # идентификатор задачи
    self.start_date = start_date         # дата старта задачи, задаваемая числом
    self.finish_date = finish_date       # дата окончания задачи, задаваемая числом
    self.duration = duration             # длительность задачи, задаваемая числом
    self.next_activity = []              # список задач-последователей
    self.prior_activity = []             # список задач-предшественников
    self.not_early_date = not_early_date # дата, раньше которой задача не может стартовать
    self.act_db = act_db

  # метод получения идентификатора задачи
  def get_id(self):
    return self.id

  # метод задания идентификатора задачи.
  # в настоящий момент не используется, т.к. изменение идентификатора недопустимо
  # def set_id(self, id):
  #   self.id = id

  # метод получения старта задачи
  def get_start_date(self):
    return self.start_date

  # метод задания старта задачи.
  # задание старта приводит к пересчету окончания задачи и стартов всех последователей и предшественников
  def set_start_date(self, start_date):
    if start_date != None and self.start_date != start_date and start_date >= 0:
      if self.prior_activity != []:
        max_finish_date = 0
        for iactivity in self.prior_activity:
          activity = self.act_db[iactivity]
          if activity.finish_date > max_finish_date:
            max_finish_date = activity.finish_date
        if start_date > max_finish_date:          
          self.set_not_early_date(start_date)          
          self.start_date = start_date
          self.finish_date = self.start_date + self.duration
          self.recalculate_next()
        elif start_date == max_finish_date:
          self.start_date = max_finish_date
          self.finish_date = self.start_date + self.duration
          self.recalculate_next() 
        else:
          pass  # выдать сообщение, что дата старта не может быть раньше даты окончания задач-предшественников
      else:
        self.set_not_early_date(start_date)
        self.start_date = start_date
        self.finish_date = self.start_date + self.duration
        self.recalculate_next()        
    else:
      pass # выдать сообщение, что дата старта не может быть пустой или меньше нуля

  # метод получения окончания задачи
  def get_finish_date(self):
    return self.finish_date

  # метод задания окончания задачи.
  # задание окончания приводит к пересчету длительности задачи и стартов всех последователей
  def set_finish_date(self, finish_date):
    if finish_date != None and finish_date - self.start_date >= 0:
      self.finish_date = finish_date
      self.duration = self.finish_date - self.start_date
      self.recalculate_next()
    else:
      pass # выдать сообщение, что дата окончания не может быть пустой или меньше даты начала

  # метод получения длительности задачи
  def get_duration(self):
    return self.duration

  # метод задания длительности задачи.
  # задание длительности приводит к пересчету окончания задачи и стартов всех последователей
  def set_duration(self, duration):
    if duration != None and duration >= 0:
      self.duration = duration
      self.finish_date = self.start_date + self.duration
      self.recalculate_next()
    else:
      pass # выдать сообщение, что длительность не может быть пустой или меньше нуля

  # метод пересчета всех последователей
  def recalculate_next(self):
    if self.next_activity != []:
      for iactivity in self.next_activity:
        activity = self.act_db[iactivity]
        max_finish_date = 0
        for iprior_activity in activity.prior_activity:
          prior_activity = self.act_db[iprior_activity]
          if prior_activity.finish_date > max_finish_date:
            max_finish_date = prior_activity.finish_date
        if (activity.not_early_date == None) or (activity.not_early_date != None and max_finish_date > activity.not_early_date):
          activity.set_start_date(max_finish_date)

  # метод получения идентификаторов задач-последоваталей
  def get_next(self):
    return [self.act_db[activity].__str__() for activity in self.next_activity]

  # метод проверки, что задача может стать последователем
  def is_valid_next_activity(self, inext_activity : int):
    next_activity = self.act_db[inext_activity]
    is_valid = False
    if next_activity != None and self != next_activity:
      is_valid = True
      # НЕ ПРОВЕРЯЕМ ЦИКЛЫ
#       if self.prior_activity != []:
#         for iprior_activity in self.prior_activity:
#           prior_activity = self.act_db[iprior_activity]
#           is_valid = prior_activity.is_valid_next_activity(inext_activity)
#           if is_valid == False:
#             break
    return is_valid

  # метод добавления ссылки на задачу-последоваталя.
  # для задачи-последователя добавляется ссылка на задачу-предшественника. это необходимо для обеспечения работы метода recalculate_next(). 
  # добавление задачи-последователя приводит к пересчету стартов всех последователей
  def append_next(self, inext_activity : int):
    next_activity = self.act_db[inext_activity]
    if self.is_valid_next_activity(inext_activity):
      if next_activity.prior_activity != []:
        max_finish_date = 0
        for iactivity in next_activity.prior_activity:
          activity = self.act_db[iactivity]
          if activity.finish_date > max_finish_date:
            max_finish_date = activity.finish_date
        if self.finish_date > max_finish_date:
          recalculate = True
        else:
          recalculate = False
      else:
        recalculate = True
      self.next_activity.append(inext_activity)
      next_activity.prior_activity.append(self.id)
      if recalculate:
        self.recalculate_next()
    else:
      pass # выдать сообщение, что эта задача не может стать последователем, т.к. является предшественником

  # метод удаления ссылки на задачу-последователя
  def remove_next(self, inext_activity : int):
    next_activity = self.act_db[inext_activity]
    if self.next_activity.count(inext_activity) > 0:
      next_activity.prior_activity.remove(self.id)
      if next_activity.prior_activity != []:
        self.act_db[(next_activity.prior_activity)[0]].recalculate_next()
      self.next_activity.remove(inext_activity)
      self.recalculate_next()
    else:
      pass # выдать сообщение, что задача не является последователем

  # метод получения даты, раньше которой задача не может стартовать
  def get_not_early_date(self):
    return self.not_early_date

  # метод задания даты, раньше которой задача не может стартовать
  def set_not_early_date(self, not_early_date):
    self.not_early_date = not_early_date
    if not_early_date != None and not_early_date > self.start_date:
      self.start_date = not_early_date
      self.finish_date = self.start_date + self.duration
      self.recalculate_next()
    if self.not_early_date == None and self.prior_activity != []:
      max_finish_date = 0
      for iactivity in self.prior_activity:
        activity = self.act_db[iactivity]
        if activity.finish_date > max_finish_date:
          max_finish_date = activity.finish_date      
      self.set_start_date(max_finish_date)

  # метод представления задачи в виде ее идентификатора
  def __str__(self):
    return f"[{self.prior_activity}] <- Task(start={self.start_date} end={self.finish_date} dur={self.duration}) -> [{self.next_activity}]"
  
  # метод представления задачи в виде ее идентификатора
  def __repr__(self):
    return f"[{self.prior_activity}] <- Task(id={self.id} start={self.start_date} end={self.finish_date} dur={self.duration}) -> [{self.next_activity}]"
