from h2o_wave import Q, ui, data
from colour import Color

def add_chart(box, title, plot_type='interval', color_gradient=True, color_n=10):
    if color_gradient:
        c2 = Color("#86003c")
        c1 = Color("#ff8ba0")
        colors = " ".join([c.hex_l for c in list(c1.range_to(c2, color_n))])

    return ui.plot_card(
        box=box,
        title=title,
        data=data('xvalue yvalue'),
        plot=ui.plot([ui.mark(type=plot_type, x='=xvalue', y='=yvalue', color='=yvalue', color_range=colors)])
    )

def add_gauge_card(box, key, value):
    return ui.tall_gauge_stat_card(
                box=box,
                title=key,
                value='={{intl value minimum_fraction_digits=2 maximum_fraction_digits=2}}',
                aux_value='',
                plot_color='$red',
                progress=value,
                data=dict(value=value),
            )

def add_stat_card(box, key, value):
    value = str(value)
    return ui.small_stat_card(
            box=box,
            title=key,
            value='={{intl value}}',
            # aux_value='',
            data = dict(value=value),
            #caption=key + " of the customer"
        )
def add_interval_card(box, title, value, plot_type='interval'):
    return ui.plot_card(
        box=box,
        title=title,
        data=data('counts division', 0),
        plot=ui.plot([ui.mark(type=plot_type, x='=division', y='=counts', y_min=0,),
                      ui.mark(x=value, label='', ref_stroke_color="#86003c", ref_stroke_size=2),])
    )

def add_area_card(box, title, value):
    return ui.plot_card(
        box=box,
        title=title,
        data=data('counts division', 0),
        plot=ui.plot([ui.mark(type="area", x='=division', y='=counts', color="#ff8ba0", y_min=0,),
                      ui.mark(type='line', x='=division', y='=counts', color='#e41f7b'),
                      ui.mark(x=value, label='', ref_stroke_color="#86003c", ref_stroke_size=2),])
    )

def add_markdown(box, key, value):
    return ui.markup_card(
        box=box,
        title=key,
        content=value,
    )


def add_header_card(box):
    return ui.header_card(box=box, 
                icon='UserFollowed', 
                icon_color='Black',
                title="Credit Risk Wave Application",
                subtitle="Generate Default Probability Predictions using Driverless AI" )

def add_sidebar_card(box, customer_ids, customer_names, customer_id, endpoint):
    id_choices = [ui.choice(str(id), str(id) + ": "+name) for id, name in zip(customer_ids, customer_names)]
    return ui.form_card(box=box,
                        items=[ui.text_xl(content='Select Customer'),
                               ui.dropdown(name='customer_id', label='Customer', choices=id_choices, value=customer_id),
                               ui.textbox(name='endpoint', label='MLOps Endpoint', value=endpoint, placeholder="URL to MLOps deployment"),
                               ui.button(name='predict', label='Generate', primary=True)
                               ])

def add_error_message(q, type, message):
    q.page['error_message'] = ui.form_card(
        box='1 5 2 2',
        items=[
            ui.message_bar(type=type, text=message),
        ]
    )
def add_text_card(box, text):
    return ui.form_card(box=box, items = [ui.text_l(text)])
