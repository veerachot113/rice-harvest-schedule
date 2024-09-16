classDiagram
    direction LR

    class CustomUser {
        +CharField user_type
        +CharField first_name
        +CharField last_name
        +CharField address
        +CharField phone
        +EmailField email
        +BooleanField is_staff
        +ManyToManyField groups
        +ManyToManyField user_permissions
        +str __str__()
    }

    class Group {
        +CharField name
        +ManyToManyField permissions
    }

    class Permission {
        +CharField name
    }

    class DriverDocument {
        +ForeignKey driver
        +ImageField id_card
        +ImageField car_registration
        +ImageField driver_with_car
        +DateTimeField submission_date
        +CharField request_status
        +TextField note
        +DateTimeField response_date
        +str __str__()
    }

    class Vehicle {
        +OneToOneField driver
        +CharField model
        +CharField type
        +DecimalField price
        +CharField province
        +ImageField image
        +IntegerField min_acres
        +IntegerField max_acres_per_day
        +BooleanField status
        +str __str__()
    }

    class CalendarEvent {
        +ForeignKey driver
        +CharField title
        +TextField details
        +DateTimeField start
        +DateTimeField end
        +ForeignKey farmer
        +CharField google_event_id
        +str __str__()
    }

    class HarvestArea {
        +ForeignKey driver
        +DateField start_date
        +DateField end_date
        +CharField province
        +CharField district
        +CharField subdistrict
        +TextField details
        +str __str__()
    }

    class VehicleDetail {
        +ForeignKey vehicle
        +CharField power
        +ImageField image1
        +ImageField image2
        +ImageField image3
        +TextField details
        +str __str__()
    }

    CustomUser "1" --* "0..*" Group : belongs to
    CustomUser "1" --* "0..*" Permission : has
    CustomUser "1" -- "0..*" DriverDocument : submits
    CustomUser "1" -- "0..1" Vehicle : owns
    CustomUser "1" -- "0..*" CalendarEvent : has events
    CustomUser "1" -- "0..*" HarvestArea : harvests in
    Vehicle "1" -- "0..*" VehicleDetail : has details
    CustomUser "1" -- "0..*" CalendarEvent : attends
