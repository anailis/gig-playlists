package me.eilidhfummey.gigplaylists.controller;

import me.eilidhfummey.gigplaylists.model.Gig;
import org.mockito.Mock;
import org.springframework.data.repository.CrudRepository;

class GigControllerTest {

    @Mock
    CrudRepository<Gig, Long> gigRepository;
}