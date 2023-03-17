export function connect(){
    const sb = useSupabaseClient();
    return sb;
}

export async function getdata(query: string, where: string, what: string) {
    const l = await connect().from("schedule");

    let data = await l.select(query).eq(where, what).order("id", {ascending: false});
    // @ts-ignore
    return data["data"]![0][query];
}

export async function datafetch(query: string) {
    const l = await connect().from("schedule");
    let data = await l.select(query).order("id", {ascending:false});
    return data["data"]
}
