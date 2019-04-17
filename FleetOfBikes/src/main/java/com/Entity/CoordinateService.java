package com.Entity;

import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.HashMap;

@Service
public class CoordinateService {

    private HashMap<String, Coordinate> coords = new HashMap<>();

    public void addCoord(Coordinate coord) {
        coords.put(coord.getName(), coord);
    }

    public HashMap<String, Coordinate> getCoords() {
        return coords;
    }

    public Coordinate getCoord(String bikeName) {
        return coords.get(bikeName);
    }

    public Location getLocation(String bikeName) {
        return coords.get(bikeName).getLoc();
    }
}
