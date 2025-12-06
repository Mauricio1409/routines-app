
class BaseRepository:
    def __init__(self, model):
        self.model = model

    def get_all(self):
        return self.model.objects.all()

    def get_by_id(self, pk):
        return self.model.objects.filter(id=pk).first()

    def create(self, data):
        return self.model.objects.create(**data)

    def update(self, instancia, data):
        for key, value in data.items():
            setattr(instancia, key, value)
        instancia.save()
        return instancia

    def delete(self, instancia):
        instancia.delete()





