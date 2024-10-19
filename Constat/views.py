from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import fitz  # PyMuPDF
import base64
from django.core.files.base import ContentFile


import os
import json

from Constat.models import Constat
import json
# Disable CSRF for this view

@csrf_exempt
def get_constats(request):
    user_id = request.GET.get('cin')  # Use request.GET to access query parameters
    
    constatsAsA = Constat.objects.filter(cinA=user_id).exclude(cinB=None)
    
    # Fetch constats where user is cinB and cinA is not None
    constatsAsB = Constat.objects.filter(cinB=user_id).exclude(cinA=None)
    
    # Combine the two querysets
    constatscompleted = constatsAsA.union(constatsAsB)
    constatsAsA = Constat.objects.filter(cinA=user_id,cinB=None)
    
    # Fetch constats where user is cinB and cinA is not None
    constatsAsB = Constat.objects.filter(cinB=user_id,cinA=None)

    # Combine the two querysets
    constatsnoncompleted = constatsAsA.union(constatsAsB)


    

    
    # Prepare data for response
    constats_data = [
        {
            'id': constat.id,
            'codeA': constat.codeA,
            'codeB': constat.codeB,
            'cinA': constat.cinA,
            'cinB': constat.cinB,
            'created_at': constat.created_at
        }
        for constat in constatscompleted
    ]

    constats_dat_noncompleted = [
        {
            'id': constat.id,
            'codeA': constat.codeA,
            'codeB': constat.codeB,
            'cinA': constat.cinA,
            'cinB': constat.cinB,
            'created_at': constat.created_at
        }
        for constat in constatsnoncompleted
    ]
    
    return JsonResponse([{"completed":constats_data,"noncompleted":constats_dat_noncompleted}], safe=False)





@csrf_exempt
def create_constat(request):
    if request.method == 'POST':
        try:
            # Parse the JSON body
            data = json.loads(request.body)
            code = data.get('code')
            cin = data.get('cin')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        if not code:
            return JsonResponse({'error': 'Code is required'}, status=400)
        
        # Try to get or create the Constat object
        constat, created = Constat.objects.get_or_create(codeA=code, cinA=cin)
        
        if not created:  # If the object already exists, check the codeB logic
            if constat.codeA == code:
                if constat.codeB is None:  # Ensure codeB is empty before updating
                    constat.codeB = code
                    constat.cinB = cin
                    constat.save()
                    return JsonResponse({'message': 'Constat updated successfully with Code B'})
                else:
                    return JsonResponse({'error': 'Code B is already set'}, status=400)
            else:
                return JsonResponse({'error': 'Code B does not match Code A'}, status=400)
        else:
            # Return a message indicating the Constat was created
            return JsonResponse({'message': 'Constat created successfully', 'constat_id': constat.id})
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)
@csrf_exempt
def update_constat_with_codeb(request, constat_id):
    if request.method == 'POST':
        code_b = request.POST.get('code')
        
        if not code_b:
            return JsonResponse({'error': 'Code B is required'}, status=400)
        
        constat = get_object_or_404(Constat, id=constat_id)
        
        if code_b != constat.codeA:
            return JsonResponse({'error': 'Code B does not match Code A'}, status=400)
        
        constat.codeB = code_b
        constat.save()
        
        return JsonResponse({'message': 'Constat updated successfully with Code B'})


def parse_coordinates(coord_str):
    x, y = map(float, coord_str.split('/'))
    return x, y



@csrf_exempt
def update_constat_with_file(request, constat_id, type, cin):
    if request.method == 'POST':
        try:
            datarequest = json.loads(request.body)
            data = json.loads(datarequest.get('data'))
            cors = datarequest.get('cors')
            signature = datarequest.get('signature')
            croquis = datarequest.get('croquis')
            corscroquis = datarequest.get('corscroquis')
            

            print(cors)
            print(data)

            # Decode the base64 signature and create an image
            signature_image = base64.b64decode(signature)
            temp_image_path = "Constat/static/signature.png"
            with open(temp_image_path, 'wb') as f:
                f.write(signature_image)
            croquis_image = base64.b64decode(croquis)
            temp_image_path_croquis = "Constat/static/croquis.png"
            with open(temp_image_path_croquis, 'wb') as f:
                f.write(croquis_image)

            # Open an existing PDF or create a new one
            doc = fitz.open("Constat/constat.pdf")
            page = doc[0]  # Assuming you're working on the first page of the PDF

            if not constat_id:
                return JsonResponse({'error': 'Code is required'}, status=400)

            constat = get_object_or_404(Constat, codeA=constat_id)

            dir = "/media/"
            os.makedirs(dir, exist_ok=True)

            filepath = os.path.join(dir, f"{constat_id}.json")

            if type == "A":
                for obj in data:
                    x, y = parse_coordinates(obj["cor"])
                    page.insert_text((x, y), obj["data"], fontsize=8)
                
                if signature:
                    # Insert the signature image into the PDF
                    # Define the rectangle: (x0, y0, x1, y1)
                    # Adjust the width and height (e.g., 100x50) as needed
                    signature_rect = fitz.Rect(90, 760, 190, 790)  # Example: width=100, height=50
                    page.insert_image(signature_rect, filename=temp_image_path)
                if croquis:
                    # Insert the signature image into the PDF
                    # Define the rectangle: (x0, y0, x1, y1)
                    # Adjust the width and height (e.g., 100x50) as needed
                    croquis_rect = fitz.Rect(170, 604, 430, 698) 
                     # Example: width=100, height=50
                    page.insert_image(croquis_rect, filename=temp_image_path_croquis,rotate=180)   

                doc.save(os.path.join(dir, f"{constat_id}_output_A.pdf"))
                constat.vehicleA = filepath
                constat.save()

            elif type == "B":
                for obj in data:
                    x, y = parse_coordinates(obj["cor"])
                    page.insert_text((x, y), obj["data"], fontsize=8)

                if signature:
                    # Insert the signature image into the PDF
                    signature_rect = fitz.Rect(412, 760, 512, 810) 
                    
                     # Example: width=100, height=50
                    page.insert_image(signature_rect, filename=temp_image_path)

                doc.save(os.path.join(dir, f"{constat_id}_output_B.pdf"))
                constat.vehicleB = filepath
                constat.save()

            doc.close()

            return JsonResponse({'message': 'Constat updated successfully'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)



# @csrf_exempt
# def writeonPDF(request):

#     if request.method == 'POST':
#         data = json.loads(request.body)
#         code = data.get('code')
#         cin = data.get('cin')

#         FolderA = "Constat/static/constat_vehicleA/"
#         FolderB = "Constat/static/constat_vehicleB/"



#         pdf_file = "../assets/constat.pdf"
#         c = canvas.Canvas(pdf_file, pagesize=A4)
#         width, height = A4

#         # Function to parse coordinates
#         def parse_coordinates(coord_str):
#             x, y = map(float, coord_str.split('/'))
#             return x, y
        
#         x, y = parse_coordinates(corA["date"])
#         c.drawString(x, height - y, f"{key}: Sample data")

        

#         # Example: Drawing values from corA onto the PDF
#         for key, coord in corA.items():
#             x, y = parse_coordinates(coord)
#             c.drawString(x, height - y, f"{key}: Sample data")

#         # Save the PDF
#         c.save()
#         print(f"PDF saved as {pdf_file}")





