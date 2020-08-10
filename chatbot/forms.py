from django import forms


class BookingForm(forms.Form):
    round_date = forms.DateField(required=True)

    round_time = forms.TimeField(required=True)

    pax = forms.ChoiceField(choices=(), required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)

        super(BookingForm, self).__init__(*args, **kwargs)

        self.fields['pax'].choices = tuple((str(i), str(i)) for i in [x for x in range(1, 6)])
