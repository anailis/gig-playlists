package me.eilidhfummey.gigplaylists.model;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

import java.time.LocalDate;

@Entity
public class Gig {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;
    private String name;
    private String spotifyArtistId;
    private LocalDate date;

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getSpotifyArtistId() {
        return spotifyArtistId;
    }

    public LocalDate getDate() {
        return date;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setSpotifyArtistId(String spotifyArtistId) {
        this.spotifyArtistId = spotifyArtistId;
    }

    public void setDate(LocalDate date) {
        this.date = date;
    }

    @Override
    public String toString() {
        return "Gig{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", spotifyArtistId='" + spotifyArtistId + '\'' +
                ", date=" + date +
                '}';
    }
}
