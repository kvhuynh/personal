package com.kevinhuynh.riotgamesstattracker.services;

import java.util.ArrayList;

import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import com.kevinhuynh.riotgamesstattracker.models.Summoner;
import com.kevinhuynh.riotgamesstattracker.repositories.SummonerRepository;

@Service
public class SummonerService {

	@Autowired
	private SummonerRepository summonerRepository;
	
	private final String API_KEY = "RGAPI-3ea3a00f-227e-4ddc-b3fb-d778edf10d06";
	
	public ArrayList<Object> getSummonerData(String summonerName) {
		String uri = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summonerName + "?api_key=" + API_KEY;
		ArrayList<Object> summonerData = new ArrayList<Object>();
		RestTemplate restTemplate = new RestTemplate();
		String result = restTemplate.getForObject(uri, String.class);
		String jsonString = result ;
		JSONObject obj = new JSONObject(jsonString);
		String id = obj.getString("id");
		String accountId = obj.getString("accountId");
		String puuid = obj.getString("puuid");
		Long level = obj.getLong("summonerLevel");
		summonerData.add(id);
		summonerData.add(accountId);
		summonerData.add(puuid);
		summonerData.add(level);
		return summonerData;
	}
	
	public Summoner toSummoner(ArrayList<Object> summonerData) {
//		System.out.println(summonerData.get(0));
//		System.out.println(summonerData.get(1));
//		System.out.println(summonerData.get(2));
//		System.out.println(summonerData.get(3));
		Summoner summoner = new Summoner();
		summoner.setAccountId((String) summonerData.get(0));
		summoner.setSummonerId((String) summonerData.get(1));
		summoner.setPuuid((String) summonerData.get(2));
		summoner.setName((String) summonerData.get(3));
		return summoner;
	}
	
	
}
