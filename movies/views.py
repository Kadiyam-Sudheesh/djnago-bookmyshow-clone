from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Theater, Seat, Booking
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction


def movie_list(request):
    search_query = request.GET.get('search')
    if search_query:
        movies = Movie.objects.filter(name__icontains=search_query)
    else:
        movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies})


def theater_list(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    theaters = Theater.objects.filter(movie=movie)
    return render(request, 'movies/theater_list.html', {'movie': movie, 'theaters': theaters})


@login_required(login_url='/login/')
def book_seats(request, theater_id):
    # FIX: consistent variable name 'theater' (singular) throughout
    theater = get_object_or_404(Theater, id=theater_id)
    seats = Seat.objects.filter(theater=theater)

    if request.method == 'POST':
        selected_seats = request.POST.getlist('seats')
        error_seats = []

        # FIX: pass correct context variable 'theater' (was 'theater' referencing undefined name)
        if not selected_seats:
            return render(request, 'movies/seat_selection.html', {
                'theaters': theater,
                'seats': seats,
                'error': 'No seat selected. Please select at least one seat.',
            })

        # FIX: use select_for_update() to prevent race conditions on concurrent bookings
        with transaction.atomic():
            for seat_id in selected_seats:
                try:
                    seat = Seat.objects.select_for_update().get(id=seat_id, theater=theater)
                except Seat.DoesNotExist:
                    continue

                if seat.is_booked:
                    error_seats.append(seat.seat_number)
                    continue

                try:
                    Booking.objects.create(
                        user=request.user,
                        seat=seat,
                        movie=theater.movie,
                        theater=theater,
                    )
                    seat.is_booked = True
                    seat.save()
                except IntegrityError:
                    error_seats.append(seat.seat_number)

        if error_seats:
            # FIX: correct string join syntax (was ',',join(...) — a tuple, not a method call)
            error_message = f"The following seats are already booked: {', '.join(error_seats)}"
            return render(request, 'movies/seat_selection.html', {
                'theaters': theater,
                'seats': Seat.objects.filter(theater=theater),  # refresh seat state
                'error': error_message,
            })

        return redirect('profile')

    return render(request, 'movies/seat_selection.html', {
        'theaters': theater,
        'seats': seats,
    })
