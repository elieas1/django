from .forms import postform,emailform

def form_processor(request):
 form = postform(auto_id=True) 
 email = emailform()   
 return {'form': form,'email':email}