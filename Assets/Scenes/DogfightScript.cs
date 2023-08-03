using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DogfightScript : MonoBehaviour
{
    public GameObject crewCardPrefab;

    public List<CrewCard> deck1;
    public List<CrewCard> deck2;



    // Start is called before the first frame update
    void Start()
    {
        Debug.Log("starting dogfight");
        for (int index = 0; index < deck1.Count; index++)
        {
            crewCardPrefab.GetComponent<CrewCardScript>().crewCard = deck1[index];

            Instantiate(crewCardPrefab, new Vector3(transform.position.x + (3 * index) - 6, transform.position.y, transform.position.z), transform.rotation);
        }
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
