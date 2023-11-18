package me.eilidhfummey.gigplaylists.controller;

import me.eilidhfummey.gigplaylists.model.Gig;
import org.springframework.data.repository.CrudRepository;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.Optional;

@RestController
@RequestMapping(value = "/gigs")
public class GigController {

    CrudRepository<Gig, Long> gigRepository;

    public GigController(CrudRepository<Gig, Long> gigRepository) {
        this.gigRepository = gigRepository;
    }

    @GetMapping(produces = "application/json")
    public Iterable<Gig> getGigs() {
        return gigRepository.findAll();
    }

    @GetMapping(value = "/{id}", produces = "application/json")
    public Optional<Gig> getGigById(@PathVariable Long id) {
        // implement not found
        return gigRepository.findById(id);
    }

    @PostMapping(produces = "text/plain")
    public void postGig() {
        Gig example = new Gig();
        example.setName("Petey");
        example.setSpotifyArtistId("4TeKBLCqmYXzvcgYX4t4YA");
        example.setDate(LocalDate.of(2023, 11, 18));
        gigRepository.save(example);
    }
}
