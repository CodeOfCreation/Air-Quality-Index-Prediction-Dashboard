from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import AQIInputForm
from .models import PredictionHistory
from .ml_service import AQIPredictor
import json

def dashboard_view(request):
    form = AQIInputForm()
    lr_prediction = None
    dt_prediction = None
    lr_category = None
    dt_category = None
    difference = None
    chart_data = None
    
    if request.method == 'POST':
        form = AQIInputForm(request.POST)
        if form.is_valid():
            # Extract features from form
            features = [
                form.cleaned_data['pm25'],
                form.cleaned_data['pm10'],
                form.cleaned_data['no2'],
                form.cleaned_data['so2'],
                form.cleaned_data['co'],
                form.cleaned_data['o3'],
                form.cleaned_data['temperature'],
                form.cleaned_data['humidity']
            ]
            
            # Get predictions from both models
            predictor = AQIPredictor()
            lr_prediction = predictor.predict(features, 'lr')
            dt_prediction = predictor.predict(features, 'dt')
            
            # Get categories
            lr_category = predictor.get_aqi_category(lr_prediction)
            dt_category = predictor.get_aqi_category(dt_prediction)
            
            # Calculate difference
            difference = abs(lr_prediction - dt_prediction)
            
            # Save to history
            PredictionHistory.objects.create(
                pm25=form.cleaned_data['pm25'],
                pm10=form.cleaned_data['pm10'],
                no2=form.cleaned_data['no2'],
                so2=form.cleaned_data['so2'],
                co=form.cleaned_data['co'],
                o3=form.cleaned_data['o3'],
                temperature=form.cleaned_data['temperature'],
                humidity=form.cleaned_data['humidity'],
                lr_prediction=lr_prediction,
                dt_prediction=dt_prediction
            )
    
    # Get recent predictions for chart
    recent_predictions = PredictionHistory.objects.all()[:10]
    chart_data = {
        'timestamps': [p.timestamp.strftime('%H:%M') for p in reversed(recent_predictions)],
        'lr_predictions': [p.lr_prediction for p in reversed(recent_predictions)],
        'dt_predictions': [p.dt_prediction for p in reversed(recent_predictions)]
    }
    
    # Get last 10 predictions for display
    recent_history = PredictionHistory.objects.all()[:10]
    
    context = {
        'form': form,
        'lr_prediction': lr_prediction,
        'dt_prediction': dt_prediction,
        'lr_category': lr_category,
        'dt_category': dt_category,
        'difference': difference,
        'chart_data': chart_data,
        'recent_history': recent_history
    }
    
    return render(request, 'dashboard/index.html', context)

def history_view(request):
    predictions = PredictionHistory.objects.all()
    paginator = Paginator(predictions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj
    }
    
    return render(request, 'dashboard/history.html', context)

@csrf_exempt
def api_predict(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            features = [
                data['pm25'],
                data['pm10'],
                data['no2'],
                data['so2'],
                data['co'],
                data['o3'],
                data['temperature'],
                data['humidity']
            ]
            
            predictor = AQIPredictor()
            lr_prediction = predictor.predict(features, 'lr')
            dt_prediction = predictor.predict(features, 'dt')
            
            lr_category = predictor.get_aqi_category(lr_prediction)
            dt_category = predictor.get_aqi_category(dt_prediction)
            
            return JsonResponse({
                'success': True,
                'predictions': {
                    'linear_regression': {
                        'aqi': lr_prediction,
                        'category': lr_category
                    },
                    'decision_tree': {
                        'aqi': dt_prediction,
                        'category': dt_category
                    }
                }
            })
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    }, status=405)
def history_view(request):
    predictions = PredictionHistory.objects.all()
    paginator = Paginator(predictions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Add difference calculation for each prediction
    for prediction in page_obj:
        prediction.difference = abs(prediction.lr_prediction - prediction.dt_prediction)
    
    context = {
        'page_obj': page_obj
    }
    
    return render(request, 'dashboard/history.html', context)