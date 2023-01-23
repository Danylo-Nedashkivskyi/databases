import model
import view
import controller

db = controller.Controller(model.Model(3), view.View)
db.menu()