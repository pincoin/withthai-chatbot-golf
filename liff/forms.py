from django import forms


class GolfBookingForm(forms.Form):
    round_date = forms.DateField(required=True)

    round_time = forms.TimeField(required=True)

    pax = forms.ChoiceField(choices=(), required=True)

    cart = forms.ChoiceField(choices=(), required=True)

    customer_name = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.golf_club = kwargs.pop('golf_club', None)

        super(GolfBookingForm, self).__init__(*args, **kwargs)

        self.fields['pax'].choices = tuple((str(i), str(i))
                                           for i in [x for x in range(1, int(self.golf_club.max_pax) + 1)])
        self.fields['cart'].choices = tuple((str(i), str(i))
                                            for i in [x for x in range(1, int(self.golf_club.max_pax) + 1)])
