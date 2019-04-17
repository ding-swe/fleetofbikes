package com.controller;

import com.Entity.Coordinate;
import com.Entity.CoordinateResponse;
import com.Entity.CoordinateService;
import com.Entity.Location;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

import java.lang.reflect.Array;
import java.net.URI;
import java.util.ArrayList;
import java.util.HashMap;


@RestController
public class BikeEndPoints {

    @Autowired
    private CoordinateService CS;

    @CrossOrigin
    @RequestMapping(value = "/testPoint", method = RequestMethod.GET)
    public HashMap<String, Coordinate> testPoint() {
        return CS.getCoords();

    }


    @CrossOrigin
    @RequestMapping(value = "/testPost", method = RequestMethod.POST, consumes = "application/json")
    public void testPost(@RequestBody Coordinate inputPayload) {
        CS.addCoord(inputPayload);
    }


    @CrossOrigin
    @RequestMapping(value = "/bike/all", method = RequestMethod.POST, consumes = "application/json")
    public void getAllBikes(@RequestBody Coordinate inputPayload) {
        CS.addCoord(inputPayload);
    }

    @CrossOrigin
    @RequestMapping(value = "/bike/{bikeName}", method = RequestMethod.GET)
    public Coordinate getOneBike(@PathVariable String bikeName) {
        return CS.getCoord(bikeName);
    }

    @CrossOrigin
    @RequestMapping(value = "/bike/location/{bikeName}", method = RequestMethod.GET)
    public Location getLocationOneBike(@PathVariable String bikeName) {
        return CS.getLocation(bikeName);
    }




}
