from django import forms

class AQIInputForm(forms.Form):
    pm25 = forms.FloatField(
        label='PM2.5 (μg/m³)',
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter PM2.5 value',
            'step': '0.1'
        })
    )
    
    pm10 = forms.FloatField(
        label='PM10 (μg/m³)',
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter PM10 value',
            'step': '0.1'
        })
    )
    
    no2 = forms.FloatField(
        label='NO2 (μg/m³)',
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter NO2 value',
            'step': '0.1'
        })
    )
    
    so2 = forms.FloatField(
        label='SO2 (μg/m³)',
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter SO2 value',
            'step': '0.1'
        })
    )
    
    co = forms.FloatField(
        label='CO (mg/m³)',
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter CO value',
            'step': '0.01'
        })
    )
    
    o3 = forms.FloatField(
        label='O3 (μg/m³)',
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter O3 value',
            'step': '0.1'
        })
    )
    
    temperature = forms.FloatField(
        label='Temperature (°C)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter temperature',
            'step': '0.1'
        })
    )
    
    humidity = forms.FloatField(
        label='Humidity (%)',
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter humidity percentage',
            'step': '0.1'
        })
    )